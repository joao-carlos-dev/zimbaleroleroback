from django.urls import path
from .views import PostCreateView, PostListView, LikePostView

urlpatterns = [
    path("create/", PostCreateView.as_view(), name="create_post"),
    path("feed/", PostListView.as_view(), name="post_feed"),
    path("<int:post_id>/like/", LikePostView.as_view(), name="like_post"),
]
