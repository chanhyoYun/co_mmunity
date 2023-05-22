from rest_framework import serializers
from . models import comments

class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = comments
        fields = ("content",)