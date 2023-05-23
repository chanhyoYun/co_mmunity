from django.db import models
from users. models import users
# Create your models here.
class comments(models.Model):
    auther = models.ForeignKey(users, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

