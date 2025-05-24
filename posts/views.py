from rest_framework.views import APIView
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from accounts import serializers
from .models import Post, Like, Comment
from .serializers import PostSerializer, CommentSerializer


class PostPagination(PageNumberPagination):
    page_size = 7


class PostCreateView(generics.CreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PostListView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = PostPagination

    def get_queryset(self):
        user = self.request.user
        followed_user_ids = []

        if hasattr(user, "following"):
            try:
                followed_user_ids = list(
                    user.following.values_list("following_id", flat=True)
                )
            except Exception as e:
                print(f"Erro ao obter 'following_id' de user.following: {e}")
                pass

            user_ids_for_feed = set(followed_user_ids)
            user_ids_for_feed.add(user.id)

            querset = (
                Post.objects.filter(user_id__in=list(user_ids_for_feed))
                .select_related("user")
                .order_by("-created_at")
            )

            return querset


class PostDetailView(generics.RetrieveAPIView):
    queryset = Post.objects.all().select_related("user")
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]


class LikePostView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, post_id):
        post = Post.objects.get(id=post_id)
        like, created = Like.objects.get_or_create(user=request.user, post=post)

        if not created:
            # Se já curtiu, remove (descurte)
            like.delete()
            return Response(
                {"message": "Descurtido", "liked": False}, status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"message": "Curtido", "liked": False}, status=status.HTTP_201_CREATED
            )


class CommentCreateView(generics.CreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # post = Post.objects.get(pk=self.kwargs["post_id"])
        # serializer.save(user=self.request.user, post=post)
        try:
            post = Post.objects.get(pk=self.kwargs["post_id"])
        except Post.DoesNotExist:
            raise serializers.ValidationError({"post": "Post não encontrado"})

        serializer.save(user=self.request.user, post=post)


# Listar comentários de um post
class CommentListView(generics.ListAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = PostPagination

    def get_queryset(self):
        post_id = self.kwargs["post_id"]
        # return Comment.objects.filter(post_id=post_id).order_by("-created_at")
        return (
            Comment.objects.filter(post_id=post_id)
            .select_related("user")
            .order_by("-created_at")
        )


class CommentUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


class CommentDeleteView(generics.DestroyAPIView):
    queryset = Comment.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


class PostUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).select_related("user")


class PostDeleteView(generics.DestroyAPIView):
    queryset = Post.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


class FollowingFeedView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = PostPagination

    def get_queryset(self):
        # user = self.request.user
        # following_users = user.following.values_list("following_id", flat=True)
        # return Post.objects.filter(user__id__in=following_users).order_by("-created_at")
        user = self.request.user
        following_user_ids = []
        if hasattr(user, "following"):
            try:
                following_user_ids = list(
                    user.following.values_list("following_id", flat=True)
                )
            except Exception as e:
                print(
                    f"Erro ao obter 'following_id' de user.following em FollowingFeedView: {e}"
                )
                pass

            if not following_user_ids:
                return (
                    Post.objects.none()
                )  # Retorna queryset vazio se não segue ninguém ou erro

        return (
            Post.objects.filter(user__id__in=following_user_ids)
            .select_related("user")
            .order_by("-created_at")
        )
