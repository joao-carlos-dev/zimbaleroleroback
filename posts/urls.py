from django.urls import path
from .views import (
    PostCreateView,
    PostListView,
    LikePostView,
    CommentListView,
    CommentCreateView,
    PostUpdateView,
    PostDeleteView,
    CommentUpdateView,
    CommentDeleteView,
    FollowingFeedView,
)

urlpatterns = [
    path("create/", PostCreateView.as_view(), name="create_post"),
    path("feed/", PostListView.as_view(), name="post_feed"),
    path("<int:post_id>/like/", LikePostView.as_view(), name="like_post"),
    path("<int:post_id>/comments/", CommentListView.as_view(), name="list_comments"),
    path(
        "<int:post_id>/comments/create/",
        CommentCreateView.as_view(),
        name="create_comment",
    ),
    path("<int:pk>/update/", PostUpdateView.as_view(), name="update_post"),
    path("<int:pk>/delete/", PostDeleteView.as_view(), name="delete_post"),
    path(
        "comments/<int:pk>/update/", CommentUpdateView.as_view(), name="update_comment"
    ),
    path(
        "comments/<int:pk>/delete/", CommentDeleteView.as_view(), name="delete_comment"
    ),
]

urlpatterns += [
    path("feed/following/", FollowingFeedView.as_view(), name="following_feed"),
]
