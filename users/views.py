from users.serializers import SignupSerializer, UserViewSerializer
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from users.models import MyUser

from article.models import Articles
from article.serializer import ArticleListSerializer

class SignupView(APIView):
    """회원가입 뷰

    회원가입을 처리하는 클래스
    """
    serializer_class = SignupSerializer
    def post(self, request):
        """회원가입
        
        Args:
            request : email, password, profile_image(키워드)를 입력 받음

        Returns:
            정상 201 : 회원가입완료
            오류 400 : 회원가입실패
        """
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "회원가입 완료"}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileView(APIView):
    """회원 정보

    Args:
        APIView (get) : 회원정보 보기
        APIView (put) : 회원정보 수정
        APIView (delete) : 회원탈퇴(비활성화)
    """
    def get(self, request, user_id):
        """회원정보 조회
        
        Args:
            user_id : 회원 고유 아이디(pk)
            
        Returns:
            정상 200 : 회원정보 반환
        
        """
        user = get_object_or_404(MyUser, pk=user_id)
        serializer = UserViewSerializer(user)
        articles = Articles.objects.filter(author_id=user_id)
        article = ArticleListSerializer(articles, many=True)
        articles_like = Articles.objects.filter(likes__id=user_id)
        article_like = ArticleListSerializer(articles_like, many=True)
        return Response({"가입정보":serializer.data, "게시글":article.data, "좋아요 게시글":article_like.data}, status=status.HTTP_200_OK)

    def put(self, request, user_id):
        """회원정보 수정하기
        
        Args:
            request : profile_image(키워드), profile_image_image(이미지), profile_image_url(키워드 url) 데이터 입력 받음
            user_id : 회원 고유 아이디(pk)
        
        Returns:
            정상 202 : 수정완료
            오류 400 : 수정불가
        
        """
        user = get_object_or_404(MyUser, pk=user_id)
        serializer = SignupSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, user_id):
        """회원탈퇴

        Args:
            user_id : 회원 고유 아이디(pk)

        Returns:
            정상 200 : 탈퇴완료
        """
        user = get_object_or_404(MyUser, pk=user_id)
        user.is_active = False
        user.save()
        return Response("회원탈퇴가 완료되었습니다", status=status.HTTP_200_OK)


class FollowView(APIView):
    """팔로잉 뷰

    Args:
        APIView (post): 팔로잉 설정, 취소
    """
    def post(self, request, user_id):
        """팔로잉 함수

        Args:
            user_id : 회원 고유 아이디(pk)

        Returns:
            정상 200 : 팔로잉, 팔로잉 취소 반환
        """
        you = get_object_or_404(MyUser, id=user_id)
        me = request.user
        if me in you.followers.all():
            you.followers.remove(me)
            return Response("unfollow", status=status.HTTP_200_OK)
        else:
            you.followers.add(me)
            return Response("follow", status=status.HTTP_200_OK)
