from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    # 성/이름 구분 없는 통합 이름 필드 추가
    name = models.CharField(max_length=100, blank=True) 
    
    description = models.TextField(blank=True) 
    profile_image = models.ImageField(upload_to='users/profile/', blank=True, null=True)

    following = models.ManyToManyField(
        'self', 
        symmetrical=False, 
        related_name='followers',
        blank=True
    )

    def __str__(self):
        return self.username