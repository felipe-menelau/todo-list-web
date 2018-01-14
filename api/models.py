from django.db import models
from django.contrib.auth.models import User

class TODOList(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    title = models.CharField(max_length=100)

