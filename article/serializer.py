from rest_framework import serializers
from . models import Comments, Articles

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = "__all__"

class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = ("content",)

class ArticleSerializer(serializers.ModelSerializer):
    comment = CommentSerializer(many=True)
    class Meta:
        model = Articles
        fields = "__all__"


class ArticleCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Articles
        fields = ("title","content","image")

class ArticleListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Articles
        fields = "__all__"

