from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.utils import timezone
from datetime import timedelta
from .models import Post, Comment
from .forms import PostForm, CommentForm
from stories.models import Story # stories 모델 import 필수!
import json
from django.http import JsonResponse

@login_required
def post_list(request):
    # 1. 팔로잉 유저 리스트
    followings = request.user.following.all()
    
    # 2. 게시글 가져오기 (기존 로직)
    posts = Post.objects.filter(
        author__in=followings
    ) | Post.objects.filter(
        author=request.user
    )
    posts = posts.order_by('-created_at').distinct()
    
    # 3. 스토리 가져오기 (24시간 이내, 팔로잉 + 나) - [추가된 부분]
    time_threshold = timezone.now() - timedelta(hours=24)
    
    stories = Story.objects.filter(
        created_at__gte=time_threshold,
        author__in=followings
    ) | Story.objects.filter(
        created_at__gte=time_threshold,
        author=request.user
    )
    stories = stories.order_by('-created_at').distinct()

    return render(request, 'posts/post_list.html', {'posts': posts, 'stories': stories})

# 2. 게시글 작성
@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('posts:post_list')
    else:
        form = PostForm()
    return render(request, 'posts/post_form.html', {'form': form})

# 3. 게시글 수정
@login_required
def post_update(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user:
        return redirect('posts:post_list')
        
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('posts:post_list')
    else:
        form = PostForm(instance=post)
    return render(request, 'posts/post_form.html', {'form': form})

# 4. 게시글 삭제
@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author == request.user:
        post.delete()
    return redirect('posts:post_list')

# 5. 댓글 작성
@login_required
def comment_create(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
    return redirect('posts:post_list')

# 6. 댓글 수정
@login_required
def comment_update(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if comment.author != request.user:
        return redirect('posts:post_list')

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('posts:post_list')
    else:
        form = CommentForm(instance=comment)
    return render(request, 'posts/comment_form.html', {'form': form})

# 7. 댓글 삭제
@login_required
def comment_delete(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if comment.author == request.user:
        comment.delete()
    return redirect('posts:post_list')

# 8. 좋아요 (Ajax)
@login_required
@require_POST
def post_like_ajax(request):
    data = json.loads(request.body)
    post_id = data.get('post_id')
    post = get_object_or_404(Post, pk=post_id)
    
    if post.like_users.filter(pk=request.user.pk).exists():
        post.like_users.remove(request.user)
        is_liked = False
    else:
        post.like_users.add(request.user)
        is_liked = True
    
    context = {
        'is_liked': is_liked,
        'like_count': post.like_users.count(),
    }
    return JsonResponse(context)