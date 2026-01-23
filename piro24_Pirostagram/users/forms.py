from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        
        fields = ('name', 'username', 'description', 'profile_image')
        
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': '성명'}), 
            'username': forms.TextInput(attrs={'placeholder': '사용자 이름 (ID)'}),
            'description': forms.Textarea(attrs={'placeholder': '소개글 (선택사항)', 'rows': 3}),
        }