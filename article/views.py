from rest_framework.views import APIView
from . models import Articles, comments
from . serializer import CommentCreateSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import get_object_or_404
# Create your views here.

class Comments(APIView):
    def post(self, request, article_id):
        serializer = CommentCreateSerializer(dtaa=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, articles_id=article_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class DetailComments(APIView):
    def patch(self, request, comment_id):
        comment = get_object_or_404(Comments, id=comment_id)
        if request.user == comment.user:
            serializer = CommentCreateSerializer(comment, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response('권한이 없다.', status=status.HTTP_403_FORBIDDEN)
        
    def delete(self, request, comment_id):
        comment = get_object_or_404(Comments,id = comment_id)
        if request.user == comment.user:
            comment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response('권한이 없다.', status=status.HTTP_403_FORBIDDEN)
        
# class LikeView(APIView):  #좋아요 기능. 현재 Article모델이 없어서 주석처리
#     def post(self, request, article_id):
#         article = get_object_or_404(Article, id=article_id)
#         if request.user in article.likes.all():
#             article.likes.remove(request.user)
#             return Response("like",status=status.HTTP_204_NO_CONTENT)
#         else:
#             article.likes.add(request.user)
#             return Response("unlike",status=status.HTTP_204_NO_CONTENT)