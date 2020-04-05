import datetime
from rest_framework.decorators import action
from django.http import JsonResponse
from rest_framework import viewsets, permissions, generics
from django.db.models import Count
from django.utils.timezone import make_aware

from social.serializers import (
    PostSerializer,
    UserSerializer,
    UserSignUpSerializer,
    PostCreatorSerializer,
    LikesStatsSerializer,
    LikesStatsFilterSerializer,
)
from social.models import Post, Like, User


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')

    def get_permissions(self):
        if self.request.method == "POST":
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return UserSignUpSerializer
        return UserSerializer

    @action(detail=True)
    def action(self, request, *args, **kwargs):
        requested_user = self.get_object()
        requested_user_data = User.objects.filter(
            username=requested_user.username
        ).first()
        return JsonResponse(
            {
                "last_login": requested_user_data.last_login,
                "last_action": requested_user_data.last_action
            }
        )


class PostViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows posts to be viewed or edited.
    """
    queryset = Post.objects.all().order_by('-id')
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PostSerializer

    def get_serializer_class(self):
        if self.request.method == "POST":
            return PostCreatorSerializer
        return PostSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True)
    def toggle_like(self, request, *args, **kwargs):
        user = self.request.user
        post = self.get_object()
        post_like = Like.objects.filter(
            user_id=user,
            post_id=post,
        ).first()

        if post_like:
            post_like.delete()
            post.likes_amount -= 1
            post.save()

        else:
            post_like = Like(user_id=user, post_id=post)
            post.likes_amount += 1
            post.save()
            post_like.save()

        return JsonResponse({"likes_count": post.likes_amount})


class LikeStatsApiView(generics.ListAPIView):
    """
    API endpoint that allows posts to be viewed or edited.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = LikesStatsSerializer

    def get_queryset(self):
        queryset = Like.objects.all()

        filters = LikesStatsFilterSerializer(data=self.request.GET)
        if filters.is_valid():
            queryset = queryset.filter(
                updated__range=(
                    filters.validated_data['date_from'],
                    filters.validated_data['date_to']+datetime.timedelta(days=1)
                )
            ).order_by(
                '-updated__date'
            ).values(
                'updated__date'
            ).annotate(likes_count=Count('user_id'))

            return queryset

        else:
            return []
