from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone

from social.models import Post, User


class PostSerializer(serializers.HyperlinkedModelSerializer):

    likes_amount = serializers.ReadOnlyField()

    class Meta:
        model = Post
        fields = ['id', 'url', 'text', 'likes_amount', 'user', 'created']


class PostCreatorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'text']


class UserSerializer(serializers.HyperlinkedModelSerializer):
    posts = PostSerializer(many=True, read_only=True)
    last_action = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'last_action', 'posts']


class UserSignUpSerializer(serializers.HyperlinkedModelSerializer):
    """
    save new user, returns access and refresh tokens, saves last_login
    """
    tokens = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'password', 'tokens']

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
        )

        user.set_password(validated_data['password'])
        user.save()

        return user

    def get_tokens(self, user):
        refresh = RefreshToken.for_user(user)

        user.last_login = timezone.now()
        user.save()

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }


class LikesStatsFilterSerializer(serializers.Serializer):
    """
    serializer for like's statistic 'api/analitics/'
    """
    date_from = serializers.DateField()
    date_to = serializers.DateField()


class LikesStatsSerializer(serializers.Serializer):
    date = serializers.DateField(source="updated__date")
    likes_count = serializers.IntegerField()
