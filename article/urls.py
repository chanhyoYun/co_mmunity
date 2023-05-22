from django.urls import path
from . import views

urlpatterns = [
    path("<int:article_id>/comments/", views.Comments.as_view()), #특정 게시글에 코멘트 작성.
    path("<int:article_id>/comments/<comment_id>/", views.DetailComments.as_view()) # 특정 코멘트 수정, 삭제
]
