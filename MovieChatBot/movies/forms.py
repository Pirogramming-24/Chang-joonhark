from django import forms
from .models import Movie, Review

class MovieForm(forms.ModelForm):
    # 장르 선택지 정의
    GENRE_CHOICES = [
        ('액션', '액션'), ('코미디', '코미디'), ('드라마', '드라마'), 
        ('SF', 'SF'), ('로맨스', '로맨스'), ('공포', '공포'), 
        ('애니메이션', '애니메이션'), ('다큐멘터리', '다큐멘터리'), ('기타', '기타')
    ]

    # 장르 필드를 ChoiceField(선택 박스)로 재정의
    genre = forms.ChoiceField(choices=GENRE_CHOICES, label='장르', widget=forms.Select(attrs={'class': 'form-control'}))

    RATING_CHOICES = [(i, f'{i}점') for i in range(1, 6)]
    
    rating = forms.ChoiceField(
        choices=RATING_CHOICES, 
        label='나의 별점', 
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = Movie
        fields = ['title', 'release_date', 'genre', 'director', 'actors', 'runtime', 'poster_image', 'overview']
        labels = {
            'title': '영화 제목',
            'release_date': '개봉일',
            'director': '감독',
            'actors': '주연배우',
            'runtime': '러닝타임(분)',
            'poster_image': '포스터 이미지',
            'overview': '줄거리',
        }
        widgets = {
            'release_date': forms.DateInput(attrs={'type': 'date'}),
            'overview': forms.Textarea(attrs={'rows': 4}),
        }

# 리뷰 폼도 별점을 선택형으로 변경 (함께 사용하는 경우)
class ReviewForm(forms.ModelForm):
    RATING_CHOICES = [(i, f'{i}점') for i in range(1, 6)] # 1~5점
    
    rating = forms.ChoiceField(choices=RATING_CHOICES, label='별점', widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Review
        fields = ['rating', 'content']