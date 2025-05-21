from rest_framework import serializers
from .models import Post, Comment
from accounts.models import CustomUser


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "user", "post", "content", "created_at"]
        read_only_fields = ["user", "post", "created_at"]


# class PostSerializer(serializers.ModelSerializer):
#     user = serializers.StringRelatedField(read_only=True)

#     class Meta:
#         model = Post
#         fields = ["id", "user", "content", "created_at"]


class PostSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    likes_count = serializers.SerializerMethodField()
    like = serializers.SerializerMethodField()
    comments = CommentSerializer(many=True, read_only=True)
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            "id",
            "user",
            "content",
            "created_at",
            "likes_count",
            "like",
            "comments",
            "comments_count",
        ]

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_comments_count(self, obj):
        return obj.comments.count()

    def get_like(self, obj):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            return obj.likes.filter(user=request.user).exists()
        return False
