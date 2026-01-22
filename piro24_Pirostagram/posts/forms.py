from django import forms
from .models import Post, Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['image', 'content']
        widgets = {
            'content': forms.Textarea(attrs={'placeholder': '문구 입력...', 'rows': 3}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.TextInput(attrs={'placeholder': '댓글 달기...'})
        }