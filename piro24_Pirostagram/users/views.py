from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import User
from .forms import CustomUserCreationForm
from django.db.models import Q

# 1. 회원가입
def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            return redirect('users:login') 
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/signup.html', {'form': form})

# 2. 로그인
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('posts:post_list')
            
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

# 3. 로그아웃
def logout_view(request):
    logout(request)
    return redirect('users:login')

# 4. 유저 검색 (아이디 또는 이름)
def search_users(request):
    query = request.GET.get('q', '')
    if query:
        users = User.objects.filter(
            Q(username__icontains=query) | Q(first_name__icontains=query)
        )
    else:
        users = []
    return render(request, 'users/search_results.html', {'users': users, 'query': query})

# 5. 유저 프로필 및 팔로우 기능
@login_required
def profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    
    # 1. 팔로우 버튼을 눌렀을 때 (POST 요청)
    if request.method == 'POST':
        # 본인 팔로우 방지
        if request.user != user:
            # 이미 팔로우 중이면 -> 취소 (remove)
            if request.user.following.filter(id=user.id).exists():
                request.user.following.remove(user)
            # 팔로우 중이 아니면 -> 추가 (add)
            else:
                request.user.following.add(user)
        return redirect('users:profile', user_id=user.id)

    # 2. 프로필 페이지 조회 시 (팔로우 여부 확인)
    is_following = request.user.following.filter(id=user.id).exists() if request.user.is_authenticated else False
    
    context = {
        'profile_user': user,
        'is_following': is_following, # 템플릿으로 전달
        'followers_count': user.followers.count(),
        'following_count': user.following.count(),
    }
    return render(request, 'users/profile.html', context)