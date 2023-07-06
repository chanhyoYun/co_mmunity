from rest_framework.views import APIView
from . models import Articles,Comments
from . serializer import CommentCreateSerializer, ArticleCreateSerializer, ArticleListSerializer, CommentSerializer, ArticleSerializer
from rest_framework.response import Response
from rest_framework import status, filters, generics
from rest_framework.generics import get_object_or_404
from article.tts import tts


# Create your views here.

class ArticlesView(APIView):
    """게시글 뷰

    Args:
        APIView (post) : 게시글 작성하기
        APIView (get) : 전체게시글 가져오기
    """
    def post(self, request):
        """게시글 작성

        Args:
            request : title, content, image 등의 정보

        Returns:
            정상 201 : 게시글 작성완료
            오류 400 : 게시글 작성실패
        """
        serializer = ArticleCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def get(self, request):
        """게시글 불러오기

        Returns:
            정상 200 : 전체 게시글 불러오기
        """
        articles = Articles.objects.all().order_by("-created_at")
        serializer = ArticleListSerializer(articles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
            
    
class ArticleDetailView(APIView):
    """게시글 상세보기 뷰

    Args:
        APIView (get): 특정 게시글 불러오기
        APIView (patch): 특정 게시글 수정하기
        APIView (delete): 특정 게시글 삭제하기
    """
    def get(self, request, article_id):
        """게시글 불러오기

        Args:
            article_id : 게시글 고유 아이디(pk)

        Returns:
            정상 200 : 특정 게시글 반환
        """
        article = get_object_or_404(Articles, id=article_id)
        serializer = ArticleSerializer(article)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def patch(self, request, article_id):
        """게시글 수정하기

        Args:
            request : 수정할 내용
            article_id : 게시글 고유 아이디(pk)

        Returns:
            정상 200 : 게시글 수정완료
            오류 400 : 게시글 수정실패
            오류 403 : 작성자 불일치
        """
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
    """댓글 뷰

    Args:
        APIView (post): 댓글 작성
        APIView (get): 댓글 보기
    """
    def post(self, request, article_id):
        """댓글 작성

        Args:
            article_id : 게시글 고유 아이디(pk)

        Returns:
            정상 201 : 댓글 작성
            오류 400 : 댓글 작성 실패
        """
        serializer = CommentCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, article_id=article_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def get(self, request, article_id):
        """댓글 보기

        Args:
            article_id : 게시글 고유 아이디(pk)

        Returns:
            정상 200 : 특정 게시글에 작성되 전체 댓글 불러오기
        """
        article = Articles.objects.get(id = article_id)
        comments = article.comment.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
class DetailComments(APIView):
    """댓글 상세 뷰

    Args:
        APIView (patch): 댓글 수정
        APIView (delete): 댓글 삭제
    """
    def patch(self, request, comment_id, article_id):
        """댓글 수정

        Args:
            comment_id : 댓글 고유 아이디(pk)

        Returns:
            정상 200 : 댓글 수정 완료
            오류 400 : 댓글 수정 실패
            오류 403 : 댓글 작성자 불일치
        """
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
        
    def delete(self, request, comment_id, article_id):
        """댓글 삭제

        Args:
            comment_id : 댓글 고유 아이디(pk)

        Returns:
            정상 204 : 댓글 삭제
            오류 403 : 댓글 작성자 불일치
        """
        comment = get_object_or_404(Comments ,id = comment_id)
        if request.user == comment.user:
            comment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response('권한이 없다.', status=status.HTTP_403_FORBIDDEN)
        
class LikeView(APIView):
    """게시글 좋아요 뷰

    Args:
        APIView (post): 좋아요
    """
    def post(self, request, article_id):
        """좋아요 설정

        Args:
            article_id : 특정 게시글 아이디(pk)

        Returns:
            정상 200 : 좋아요, 좋아요 취소
        """
        article = get_object_or_404(Articles, id=article_id)
        serializer = ArticleListSerializer(article)
        if request.user in article.likes.all():
            article.likes.remove(request.user)
            return Response({"result": "unlike", "count":len(serializer.data['likes'])}, status=status.HTTP_200_OK)
        else:
            article.likes.add(request.user)
            return Response({"result": "like", "count":len(serializer.data['likes'])}, status=status.HTTP_200_OK)


class ArticlesSearchView(generics.ListCreateAPIView):
    """게시글 검색 뷰

    title, content, author__email 로 게시글 검색할 수 있는 클래스
    """
    search_fields = ["title", "content", "author__email"]
    filter_backends = (filters.SearchFilter,)
    
    queryset = Articles.objects.all()
    serializer_class = ArticleListSerializer
    
class TtsView(APIView):
    """글 읽어주기 뷰

    Args:
        APIView (get): 글 읽어주기
    """
    def get(self, request, article_id):
        """게시글 읽어주기

        Args:
            article_id : 게시글 고유 아이디(pk)

        Returns:
            정상 200 : 게시글 읽어주기
        """
        article = get_object_or_404(Articles, id=article_id)
        serializer = ArticleSerializer(article)
        tts(serializer.data['content'])
        return Response("tts", status=status.HTTP_200_OK)
