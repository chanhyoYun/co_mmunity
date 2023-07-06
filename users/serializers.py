from users.models import MyUser
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from drf_extra_fields.fields import Base64ImageField
from users.text_to_image import text_to_image
from django.contrib.auth import get_user_model

User = get_user_model()


class SignupSerializer(serializers.ModelSerializer):
    """유저 시리얼라이저

    회원가입, 회원정보 수정에 사용됨.
    """
    profile_image_image = Base64ImageField(required=False)
    class Meta:
        model = MyUser
        fields = ['id', 'email', 'password', 'profile_image', 'profile_image_url', 'followings', 'profile_image_image']


    def create(self, validated_data):
        validated_data['profile_image_url'] = text_to_image(validated_data['profile_image'])
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError('이미 사용 중인 이메일입니다.')
        try:
            validate_email(email)
            return email
        except ValidationError:
            raise serializers.ValidationError('유효하지 않은 이메일 형식입니다.')

    def update(self, instance, validated_data):
        instance.profile_image_image = validated_data.get('profile_image_image', instance.profile_image_image)
        instance.profile_image = validated_data.get('profile_image', instance.profile_image)
        instance.profile_image_url = text_to_image(instance.profile_image)
        instance.save()
        return instance
    
class UserViewSerializer(serializers.ModelSerializer):
    """유저 정보 보기 시리얼라이저

    단순 유저정보를 불러오기 위한 시리얼라이저
    """
    followings = SignupSerializer(many=True)
    class Meta:
        model = MyUser
        fields = ['id', 'email', 'password', 'profile_image', 'profile_image_url', 'followings', 'profile_image_image']

    
    def __str__(self):
        return self.email