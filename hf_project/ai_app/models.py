from django.db import models
from django.contrib.auth.models import User

class AIResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task_name = models.CharField(max_length=50) # 예: sentiment, summary
    input_text = models.TextField()
    output_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.task_name}"