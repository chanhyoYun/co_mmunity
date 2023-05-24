from rest_framework.views import APIView
from . models import Articles,Comments
from . serializer import CommentCreateSerializer, ArticleCreateSerializer, ArticleListSerializer, CommentSerializer,ArticleSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import get_object_or_404
from django.shortcuts import render
from PIL import Image


# 메인페이지 게시글 불러오기
def main_page(request):
    articles = Articles.objects.all()
    context = {'articles': articles}
    return render(request, 'main.html', context)

# Create your views here.

class ArticlesView(APIView):
    def post(self, request):
        serializer = ArticleCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def get(self, request):
        articles = Articles.objects.all()
        serializer = ArticleListSerializer(articles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
            
    
class ArticleDetailView(APIView):
    def get(self, request, article_id):
        article = get_object_or_404(Articles, id=article_id)
        serializer = ArticleSerializer(article)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def patch(self, request, article_id):
        article = get_object_or_404(Articles, id=article_id)
        if request.user == article.author:
            serializer = ArticleCreateSerializer(article, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response('권한이 없습니다.', status=status.HTTP_403_FORBIDDEN)
    
    def delete(self, request, article_id):
        article = get_object_or_404(Articles, id=article_id)
        if request.user == article.author:
            article.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response('권한이 없다.', status=status.HTTP_403_FORBIDDEN)

class CommentsView(APIView):
    def post(self, request, article_id):
        serializer = CommentCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, article_id=article_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def get(self, request, article_id):
        article = Articles.objects.get(id = article_id)
        comments = article.comment.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
class DetailComments(APIView):
    def patch(self, request, comment_id, article_id):
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
        
    def delete(self, request, comment_id, article_id):
        comment = get_object_or_404(Comments ,id = comment_id)
        if request.user == comment.user:
            comment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response('권한이 없다.', status=status.HTTP_403_FORBIDDEN)
        
class LikeView(APIView):  #좋아요 기능. 현재 Article모델이 없어서 주석처리
    def post(self, request, article_id):
        article = get_object_or_404(Articles, id=article_id)
        if request.user in article.likes.all():
            article.likes.remove(request.user)
            return Response("unlike",status=status.HTTP_204_NO_CONTENT)
        else:
            article.likes.add(request.user)
            return Response("like",status=status.HTTP_204_NO_CONTENT)

