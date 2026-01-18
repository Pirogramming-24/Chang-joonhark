from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import Movie, Review
from .forms import MovieForm
from django.db.models import Q, Avg 
from django.core.paginator import Paginator  

from django.http import JsonResponse
from langchain_upstage import ChatUpstage, UpstageEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from django.conf import settings
import os

def movie_list(request):
    # 1. 기본 쿼리셋 (평점 평균 계산 포함)
    movies = Movie.objects.annotate(avg_rating=Avg('reviews__rating'))

    # 2. 필터 기능 (전체 / TMDB / 직접 추가)
    filter_type = request.GET.get('filter', 'all')
    if filter_type == 'tmdb':
        movies = movies.filter(is_tmdb=True)
    elif filter_type == 'user':
        movies = movies.filter(is_tmdb=False)

    # 3. 검색 기능 (제목, 감독, 배우)
    query = request.GET.get('q')
    if query:
        movies = movies.filter(
            Q(title__icontains=query) | 
            Q(director__icontains=query) | 
            Q(actors__icontains=query)
        )

    # 4. 정렬 기능
    sort = request.GET.get('sort', 'latest') # 기본값: 최신등록순
    
    if sort == 'latest':     # 최신 등록순 (ID 역순)
        movies = movies.order_by('-pk')
    elif sort == 'title':    # 제목순
        movies = movies.order_by('title')
    elif sort == 'year':     # 최신 년도순
        movies = movies.order_by('-release_date')
    elif sort == 'rating':   # 평점순 (Review 모델의 rating 평균)
        movies = movies.order_by('-avg_rating')

    # 정렬까지 끝난 movies 변수를 페이징 처리
    paginator = Paginator(movies, 12)  # 페이지당 12개씩 보여주기
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'movies': page_obj,  # ★ 템플릿으로 보내는 변수는 그대로 'movies'로 유지해도 됨 (page_obj가 iterable하므로)
        'page_obj': page_obj, # 페이지 이동 버튼을 위해 별도로 전달
        'sort': sort,
        'filter': filter_type,
        'query': query,
    }
    return render(request, 'movies/movie_list.html', context)

# [R] 상세 조회
def movie_detail(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    avg_rating = movie.reviews.aggregate(Avg('rating'))['rating__avg']
    
    context = {
        'movie': movie,
        'avg_rating': avg_rating, # ★ 템플릿으로 전달
    }
    return render(request, 'movies/movie_detail.html', context)
    return render(request, 'movies/movie_detail.html', {'movie': movie})

@login_required
def movie_create(request):
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES)
        if form.is_valid():
            # 1. 영화 정보 먼저 저장
            movie = form.save(commit=False)
            movie.is_tmdb = False
            movie.save()

            # 2. 폼에서 '별점' 값 꺼내기
            rating = form.cleaned_data['rating']

            # 3. 자동으로 리뷰 생성 (나의 별점 저장)
            Review.objects.create(
                movie=movie,
                author=request.user,  # 현재 로그인한 유저 (로그인 상태여야 함)
                rating=rating,
                content=movie.overview # 줄거리 내용을 리뷰 내용으로도 사용 (또는 "첫 리뷰" 등으로 고정 가능)
            )

            return redirect('movies:movie_detail', pk=movie.pk)
    else:
        form = MovieForm()
    
    return render(request, 'movies/movie_form.html', {'form': form, 'action': '등록'})

# [U] 영화 수정
def movie_update(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES, instance=movie)
        if form.is_valid():
            form.save()
            return redirect('movies:movie_detail', pk=movie.pk)
    else:
        form = MovieForm(instance=movie)
    return render(request, 'movies/movie_form.html', {'form': form, 'action': '수정'})

# [D] 영화 삭제 (POST 요청만 허용)
@require_POST
def movie_delete(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    movie.delete()
    return redirect('movies:movie_list')

def chatbot(request):
    if request.method == 'POST':
        user_message = request.POST.get('message')
        
        # 1. 벡터 DB 로드
        persist_directory = os.path.join(settings.BASE_DIR, 'chroma_db')
        embeddings = UpstageEmbeddings(
            api_key=settings.UPSTAGE_API_KEY,
            model="solar-embedding-1-large"
        )
        vector_store = Chroma(
            persist_directory=persist_directory,
            embedding_function=embeddings
        )
        
        # 2. 관련 영화 검색 (Retriever)
        retriever = vector_store.as_retriever(search_kwargs={"k": 3}) # 관련성 높은 3개 찾기
        context_docs = retriever.invoke(user_message)
        context_text = "\n\n".join([doc.page_content for doc in context_docs])

        # 3. 프롬프트 구성 (시스템 메시지 설정)
        prompt = ChatPromptTemplate.from_messages([
            ("system", "당신은 영화 추천 전문가입니다. 아래의 [영화 정보]를 바탕으로 사용자의 질문에 친절하게 답변해주세요. 정보에 없는 내용은 지어내지 말고 모른다고 하세요. 답변은 한국어로 하세요."),
            ("human", "질문: {question}\n\n[영화 정보]:\n{context}")
        ])

        # 4. LLM 실행 (Solar)
        llm = ChatUpstage(api_key=settings.UPSTAGE_API_KEY, model="solar-pro")
        chain = prompt | llm | StrOutputParser()
        
        response = chain.invoke({"question": user_message, "context": context_text})
        
        return JsonResponse({'response': response})

    return render(request, 'movies/chatbot.html')