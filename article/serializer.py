from rest_framework import serializers
from .models import Comments, Articles
from django.utils.html import mark_safe
from easy_thumbnails.templatetags.thumbnail import thumbnail_url


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    def get_user(self, obj):
            return obj.user.email
    
    class Meta:
        model = Comments
        fields = "__all__"


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = ("content",)


class ArticleSerializer(serializers.ModelSerializer):
    comment = CommentSerializer(many=True)
    author = serializers.SerializerMethodField()
    def get_author(self, obj):
            return obj.author.email

    class Meta:
        model = Articles
        fields = "__all__"


class ArticleCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Articles
        fields = ("title", "content", "image")


class ArticleListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Articles
        fields = "__all__"


class ArticleSerializer(serializers.ModelSerializer):
    thumbnail = serializers.SerializerMethodField()

    def get_thumbnail(self, article):
        if article.image:
            image_url = article.image.url
            thumbnail_url = thumbnail_url(image_url, '250x250', crop='center')
            return mark_safe(f'<img src="{thumbnail_url}" alt="Thumbnail">')
        return None

    class Meta:
        model = Articles
        fields = ('id', 'title', 'content', 'thumbnail', 'created_at')
