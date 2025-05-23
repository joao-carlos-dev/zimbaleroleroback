from rest_framework import serializers
from .models import CustomUser, Follow
from django.contrib.auth import get_user_model


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ("email", "nome", "password")

    def create(self, validated_data):
        return CustomUser.objects.create_user(
            email=validated_data["email"],
            nome=validated_data["nome"],
            password=validated_data["password"],
        )


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("id", "email", "nome", "bio", "profile_image", "created_at")


User = get_user_model()


class FollowSerializer(serializers.ModelSerializer):
    follower = serializers.StringRelatedField(read_only=True)
    following = serializers.SlugRelatedField(
        slug_field="nome", queryset=User.objects.all()
    )

    class Meta:
        model = Follow
        fields = ["id", "follower", "following", "created_at"]
        read_only_fields = ["id", "follower", "created_at"]


class SimpleUserSerializer(serializers.Serializer):
    nome = serializers.CharField()

    class Meta:
        model = User
        fields = ["id", "nome"]

    # def to_representation(self, instance):
    #     return {"nome": instance}


class UserSerializer(serializers.ModelSerializer):
    is_following = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "nome", "email", "is_following"]

    def get_is_following(self, obj):
        """Retorna True se o usuário logado já segue esse usuário"""
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            return Follow.objects.filter(follower=request.user, following=obj).exists()
        return False
