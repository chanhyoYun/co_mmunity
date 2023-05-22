from rest_framework_simplejwt.views import TokenObtainPairView
from users.serializers import MyTokenObtainPairSerializer
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework import status

from users.models import MyUser
from users.serializers import UserSerializer

class ProfileView(APIView):
    def get(self, request, user_id):
        """회원정보 보기"""
        user = get_object_or_404(MyUser, pk=user_id)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, user_id):
        """회원정보 수정하기"""
        user = get_object_or_404(MyUser, pk=user_id)
        # 로그인한 유저와 페이지의 유저가 같은지 확인하는 코드 구현 필요
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

