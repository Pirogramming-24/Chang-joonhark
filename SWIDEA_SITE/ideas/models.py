from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from devtools.models import DevTool

class Idea(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to="ideas/", blank=True, null=True)
    content = models.TextField()
    interest = models.IntegerField(
        default=0,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(10),
        ],
    )
    devtool = models.ForeignKey(
        "devtools.DevTool",
        on_delete=models.PROTECT,
        related_name="ideas",
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    

class IdeaStar(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    idea = models.ForeignKey(Idea, on_delete=models.CASCADE, related_name="stars")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "idea")

