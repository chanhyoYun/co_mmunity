from rest_framework.views import APIView
from .models import comments
from .serializer import CommentCreateSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import get_object_or_404
# Create your views here.

class Comments(APIView):
    def post(self, request, article_id):
        serializer = CommentCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, articles_id=article_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class DetailComments(APIView):
    def patch(self, request, comment_id):
        comment = get_object_or_404(Comments, id=comment_id)
        if request.user == comment.auther:
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
        if request.user == comment.auther:
            comment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response('권한이 없다.', status=status.HTTP_403_FORBIDDEN)
        
        