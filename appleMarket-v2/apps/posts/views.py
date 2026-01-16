from django.shortcuts import render, redirect
from .models import Post
from .forms import PostForm

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .services.image_preprocessor import ImagePreprocessor
from .services.ocr_engine import OCREngine
from .services.nutrient_parser import NutrientParser

# apps/posts/views.py

def analyze_image(request):
    if request.method == 'POST' and request.FILES.get('image'):
        try:
            image_file = request.FILES['image']
            
            # 1. 전처리
            processed_images = ImagePreprocessor.preprocess(image_file)
            
            # 2. OCR 실행
            engine = OCREngine()
            all_texts = []
            for img in processed_images:
                extracted = engine.extract_text(img)
                all_texts.extend(extracted)
            
            # 3. 파싱
            result_data = NutrientParser.parse(all_texts)
            
            return JsonResponse(result_data)
            
        except Exception as e:
            print(f"서버 에러: {e}")
            return JsonResponse({'error': str(e)}, status=500)
            
    return JsonResponse({'error': 'No image provided'}, status=400)

    
def main(request):
    posts = Post.objects.all()

    search_txt = request.GET.get('search_txt')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    if search_txt:
        posts = posts.filter(title__icontains=search_txt)  # 대소문자 구분 없이 검색
    
    try:
        if min_price:
            posts = posts.filter(price__gte=int(min_price))
        if max_price:
            posts = posts.filter(price__lte=int(max_price))
    except (ValueError, TypeError):
        pass  # 필터를 무시하되, 기존 검색 필터를 유지

    context = {
        'posts': posts,
        'search_txt': search_txt,
        'min_price': min_price,
        'max_price': max_price,
    }
    return render(request, 'posts/list.html', context=context)

def create(request):
    if request.method == 'GET':
        form = PostForm()
        context = { 'form': form }
        return render(request, 'posts/create.html', context=context)
    else:
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        return redirect('/')

def detail(request, pk):
    target_post = Post.objects.get(id = pk)
    context = { 'post': target_post }
    return render(request, 'posts/detail.html', context=context)

def update(request, pk):
    post = Post.objects.get(id=pk)
    if request.method == 'GET':
        form = PostForm(instance=post)
        context = {
            'form': form, 
            'post': post
        }
        return render(request, 'posts/update.html', context=context)
    else:
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
        return redirect('posts:detail', pk=pk)

def delete(request, pk):
    post = Post.objects.get(id=pk)
    post.delete()
    return redirect('/')