from django.db import models

class DevTool(models.Model):
    name = models.CharField(max_length=100, unique=True)
    kind = models.CharField(max_length=100)
    content = models.TextField(blank=True)

    def __str__(self):
        return self.name

