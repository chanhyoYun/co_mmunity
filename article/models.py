from django.db import models
from users.models import MyUser
# Create your models here.
class comments(models.Model):
    auther = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
