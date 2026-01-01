from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = [
            "title", "year", "genre", "rating", "runtime", "content",
            "director", "actors",
        ]

        labels = {
            "title": "제목",
            "year": "개봉년도",
            "genre": "장르",
            "rating": "별점",
            "runtime": "러닝타임",
            "content": "리뷰",
            "director": "감독",
            "actors": "배우",
        }

        widgets = {
            "content": forms.Textarea(attrs={"rows": 8}),
        }
