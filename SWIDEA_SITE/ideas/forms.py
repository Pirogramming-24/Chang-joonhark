# ideas/forms.py
from django import forms
from .models import Idea

class IdeaForm(forms.ModelForm):
    class Meta:
        model = Idea
        fields = ["title", "image", "content", "interest", "devtool"]
        labels = {
            "title": "아이디어명",
            "image": "이미지",
            "content": "아이디어 설명",
            "interest": "아이디어 관심도 (0~10)",
            "devtool": "예상 개발툴",
        }
        widgets = {
            "interest": forms.NumberInput(attrs={
                "min": 0,
                "max": 10,
                "step": 1, 
            }),
        }

