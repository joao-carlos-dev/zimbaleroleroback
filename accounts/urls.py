from django.urls import path
from .views import RegisterView, UserSearchView
from .views import (
    RegisterView,
    ProfileView,
    FollowToggleView,
    FollowersListView,
    FollowingListView,
)

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("me/", ProfileView.as_view(), name="me"),
    path("follow-toggle/<str:nome>/", FollowToggleView.as_view(), name="follow_toggle"),
    path("search-users/", UserSearchView.as_view(), name="search_users"),
]

urlpatterns += [
    path("followers/<str:nome>/", FollowersListView.as_view(), name="followers_list"),
    path("following/<str:nome>/", FollowingListView.as_view(), name="following_list"),
]
