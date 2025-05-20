from rest_framework import serializers
from .models import Post
from accounts.models import CustomUser


class PostSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Post
        fields = ["id", "user", "content", "created_at"]


class PostSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ["id", "user", "content", "created_at", "likes_count"]

    def get_likes_count(self, obj):
        return obj.likes.count()
