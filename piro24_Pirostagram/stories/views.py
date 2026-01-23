from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.clickjacking import xframe_options_exempt
from django.utils import timezone
from datetime import timedelta
from .models import Story
from .forms import StoryForm

# 1. 스토리 작성
@login_required
def story_create(request):
    if request.method == 'POST':
        form = StoryForm(request.POST, request.FILES)
        
        # 폼 유효성 검사 (파일이 있는지 등)
        if form.is_valid():
            # 1. 폼에서 이미지를 가져오는 대신, request.FILES에서 전체 리스트를 가져옵니다.
            images = request.FILES.getlist('image')
            
            # 2. 반복문을 돌며 각각의 스토리 객체 생성
            for img in images:
                Story.objects.create(
                    author=request.user,
                    image=img
                )
            
            return redirect('posts:post_list')
    else:
        form = StoryForm()
        
    return render(request, 'stories/story_form.html', {'form': form})

# 2. 스토리 상세 뷰어 (이전/다음 넘기기 포함)
@xframe_options_exempt
@login_required
def story_view(request, story_id):
    story = get_object_or_404(Story, pk=story_id)
    
    # 24시간 이내의 유효한 스토리 리스트 (최신순)
    time_threshold = timezone.now() - timedelta(hours=24)
    followings = request.user.following.all()
    
    active_stories = (Story.objects.filter(created_at__gte=time_threshold, author__in=followings) | 
                      Story.objects.filter(created_at__gte=time_threshold, author=request.user))
    
    story_list = list(active_stories.order_by('-created_at').distinct())
    
    try:
        current_index = story_list.index(story)
    except ValueError:
        return redirect('posts:post_list')

    # 리스트 인덱스로 이전/다음 ID 계산
    next_story_id = story_list[current_index + 1].id if current_index + 1 < len(story_list) else None
    prev_story_id = story_list[current_index - 1].id if current_index - 1 >= 0 else None

    return render(request, 'stories/story_view.html', {
        'story': story,
        'next_story_id': next_story_id,
        'prev_story_id': prev_story_id,
    })

# 3. 스토리 리스트 (URL 에러 방지용, 실제로는 잘 안 쓰임)
@login_required
def story_list(request):
    return redirect('posts:post_list')