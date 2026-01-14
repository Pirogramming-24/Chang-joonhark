# posts/forms.py

from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = (
            'title', 'content', 'region', 'price', 'photo', 
            'user',              
            'nutrition_image', 'calories', 'carbohydrate', 'protein', 'fat'
        )
        
        widgets = {
            'user': forms.Select(attrs={'class': 'form-select'}),
            

            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'region': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }