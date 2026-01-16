from django.db import models
from django.contrib.auth.models import User  # Django 기본 유저 모델 불러오기

class Movie(models.Model):
    # 1. 영화 기본 정보
    title = models.CharField(max_length=200)  # 제목
    tmdb_id = models.IntegerField(unique=True, null=True, blank=True)  # TMDB ID (중복 방지용)
    
    # 2. 상세 정보
    overview = models.TextField(blank=True) # 줄거리
    release_date = models.DateField(null=True, blank=True)  # 개봉일
    genre = models.CharField(max_length=100, blank=True)  # 장르
    director = models.CharField(max_length=100, blank=True) # 감독
    actors = models.CharField(max_length=300, blank=True)   # 주연배우
    runtime = models.IntegerField(null=True, blank=True)    # 러닝타임(분)
    vote_average = models.FloatField(default=0.0)

    # 3. 포스터 (TMDB URL 또는 직접 업로드)
    poster_path = models.CharField(max_length=500, null=True, blank=True) # TMDB 포스터 URL
    poster_image = models.ImageField(upload_to='posters/', null=True, blank=True) # 직접 업로드용

    # 4. 관리용 필드
    is_tmdb = models.BooleanField(default=True) # TMDB에서 가져온 영화인지 여부
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Review(models.Model):
    # 영화와 1:N 관계 (영화가 삭제되면 리뷰도 삭제)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews')
    
    # 작성자 (User 모델과 연결, 탈퇴 시 리뷰는 유지하고 작성자를 null로 처리하거나 같이 삭제 가능)
    # 여기서는 작성자가 삭제되면 리뷰도 삭제되는 방식(CASCADE)을 씁니다.
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    
    rating = models.IntegerField()  # 별점 (1~5)
    content = models.TextField()    # 리뷰 내용
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"[{self.movie.title}] {self.author.username}님의 리뷰"