from rest_framework import generics, permissions, status, filters
from rest_framework.response import Response
from .serializers import RegisterSerializer, UserSerializer
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

    def post(self, request, nome):
        follower = request.user
        try:
            following = User.objects.get(nome=nome)
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
            return Response(
                {"detail": "Deixou de seguir.", "is_following": False},
                status=status.HTTP_200_OK,
            )

        return Response(
            {"detail": "Agora você está seguindo.", "is_following": True},
            status=status.HTTP_201_CREATED,
        )


class FollowersListView(generics.ListAPIView):
    serializer_class = SimpleUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        nome = self.kwargs["nome"]
        user = User.objects.get(nome=nome)
        # Quem segue o user (follower)
        return user.followers.all().values_list("follower__nome", flat=True)


class FollowingListView(generics.ListAPIView):
    serializer_class = SimpleUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        nome = self.kwargs["nome"]
        user = User.objects.get(nome=nome)
        # Quem o user segue (following)
        return user.following.all().values_list("following__nome", flat=True)


class UserSearchView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ["nome"]
