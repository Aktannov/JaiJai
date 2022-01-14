from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from video.filters import AnimeFilter
from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet

from video.models import Genre, Video, Anime, Comment, Favorites, Likes, Rating
from video.permissions import IsAdmin, IsAuthor
from video.serializer import GenreSerializer, VideoSerializer, AnimeSerializer, CommentSerializer, RatingSerializer


class GenreListView(ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

    def get_permissions(self):
        if self.action == 'retrieve':
            return [AllowAny()]
        else:
            return [IsAdmin()]


class AnimeListView(ModelViewSet):
    queryset = Anime.objects.all()
    serializer_class = AnimeSerializer

    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    filterset_class = AnimeFilter
    search_fields = ['name']
    ordering_fields = ['genre']


    def get_permissions(self):
        if self.action == 'retrieve':
            return [AllowAny()]
        else:
            return [IsAdmin()]

    @action(['POST'], detail=True)
    def add_to_fav(self, request, pk):
        anime = self.get_object()
        if request.user.favorites.filter(anime=anime).exists():
            return Response('Вы уже добавили в избранное')
        Favorites.objects.create(anime=anime, user=request.user)
        return Response('Добавлено в избранное')

    @action(['POST'], detail=True)
    def remove_from_fav(self, request, pk):
        anime = self.get_object()
        if not request.user.favorites.filter(anime=anime).exists():
            return Response('Аниме не в списке избранных')
        request.user.favorites.filter(anime=anime).delete()
        return Response('Аниме удален из избранных')




class VideoListView(ModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer

    def get_permissions(self):
        if self.action == 'retrieve':
            return [AllowAny()]
        else:
            return [IsAdmin()]

    @action(['POST'], detail=True)
    def add_to_liked(self, request, pk):
        video = self.get_object()
        if not request.user.liked.filter(video=video).exists():
            return Response('Вы уже лайкнули')
        Likes.objects.create(video=video, user=request.user)
        return Response('Вы лайкнули')

    @action(['POST'], detail=True)
    def remove_from_liked(self, request, pk):
        video = self.get_object()
        if not request.user.liked.filter(video=video).exists():
            return Response('Вы не лайкнули')
        request.user.liked.filter(video=video).delete()
        return Response('Вы убрали лайк')



class CommentListView(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated()]
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthor()]
        return [AllowAny()]


class RatingListView(ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated()]
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthor()]
        return [AllowAny()]
