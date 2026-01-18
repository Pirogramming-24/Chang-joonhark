from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import UserCreationForm

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)  # 가입 후 즉시 로그인 처리
            return redirect('movies:movie_list')
    else:
        form = UserCreationForm()
    
    context = {
        'form': form,
    }
    return render(request, 'accounts/signup.html', context)