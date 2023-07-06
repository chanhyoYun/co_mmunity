from django.db import models
from users. models import MyUser
# Create your models here.

class Articles(models.Model):
    """게시글 모델

    Args:
        author (ForeignKey) : 게시글 작성한 유저정보
        title (CharField) : 게시글 제목
        content (TextField) : 게시글 내용
        image (ImageField) : 게시글에 첨부할 사진
        created_at (DateTimeField) : 게시글 작성일자
        updated_at (DateTimeField) : 게시글 수정일자
        likes (ManyToManyField) : 게시글 좋아요
    """
    author = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    image = models.ImageField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(MyUser, blank=True, related_name="article")

class Comments(models.Model):
    """댓글 모델

    Args:
        article (ForeignKey) : 게시글 정보
        user (ForeignKey) : 댓글작성 유저 정보
        content (TextField) : 댓글 내용
        created_at (DateTimeField) : 댓글 작성일자
        updated_at (DateTimeField) : 댓글 수정일자
    """
    article = models.ForeignKey(Articles, on_delete=models.CASCADE, related_name='comment')
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

