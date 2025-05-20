from django.urls import path
from .views import RegisterView
from .views import RegisterView, ProfileView, FollowToggleView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("follow/<str:username>/", FollowToggleView.as_view(), name="follow_toggle"),
]
