from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .serializers import RegisterSerializer
from .models import CustomUser, Follow
from .serializers import UserProfileSerializer, FollowSerializer, SimpleUserSerializer
from django.contrib.auth import get_user_model


class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class ProfileView(generics.RetrieveAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


User = get_user_model()


class FollowToggleView(generics.GenericAPIView):
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, username):
        follower = request.user
        try:
            following = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response(
                {"detail": "Usuário não encontrado."}, status=status.HTTP_404_NOT_FOUND
            )

        if follower == following:
            return Response(
                {"detail": "Você não pode seguir a si mesmo."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        follow_obj, created = Follow.objects.get_or_create(
            follower=follower, following=following
        )

        if not created:
            follow_obj.delete()
            return Response({"detail": "Deixou de seguir."}, status=status.HTTP_200_OK)

        return Response(
            {"detail": "Agora você está seguindo."}, status=status.HTTP_201_CREATED
        )


class FollowersListView(generics.ListAPIView):
    serializer_class = SimpleUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        username = self.kwargs["username"]
        user = User.objects.get(username=username)
        # Quem segue o user (follower)
        return user.followers.all().values_list("follower__username", flat=True)


class FollowingListView(generics.ListAPIView):
    serializer_class = SimpleUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        username = self.kwargs["username"]
        user = User.objects.get(username=username)
        # Quem o user segue (following)
        return user.following.all().values_list("following__username", flat=True)
