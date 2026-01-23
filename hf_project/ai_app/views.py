from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse
from .services import get_ai_response
from .models import AIResult

from django.contrib.auth.forms import UserCreationForm

def process_ai_request(request, task_name, template_name):
    result = None
    history = []

    if request.method == 'POST':
        input_text = request.POST.get('input_text')
        
        # 1. AI 실행
        if input_text:
            result = get_ai_response(task_name, input_text)
            
            # 2. 로그인 상태라면 DB 저장
            if request.user.is_authenticated:
                AIResult.objects.create(
                    user=request.user,
                    task_name=task_name,
                    input_text=input_text,
                    output_text=result
                )
            
            # 3. [핵심] AJAX 요청이면 JSON으로 응답 (새로고침 방지)
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'success',
                    'result': result,
                    'input_text': input_text # 히스토리 추가용
                })

    # 일반 접속(GET)이거나 AJAX가 아닌 경우 기존대로 HTML 렌더링
    if request.user.is_authenticated:
        history = AIResult.objects.filter(
            user=request.user, 
            task_name=task_name
        ).order_by('-created_at')

    context = {
        'task_name': task_name,
        'result': result,
        'history': history,
    }
    return render(request, template_name, context)

def sentiment_view(request):
    return process_ai_request(request, 'sentiment', 'sentiment.html')

@login_required
def summary_view(request):
    return process_ai_request(request, 'summary', 'summary.html')

@login_required
def translate_view(request):
    return process_ai_request(request, 'translate', 'translate.html')

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            next_url = request.GET.get('next', '/sentiment/')
            return redirect(next_url)
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    
    return render(request, 'signup.html', {'form': form})