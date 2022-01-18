from django.urls import path, include
from rest_framework.routers import SimpleRouter

from video.views import GenreListView, AnimeListView, VideoListView, CommentListView, RatingListView, \
    TopListView, FavListView

router = SimpleRouter()
router.register('genre', GenreListView)
router.register('anime', AnimeListView)
router.register('video', VideoListView)
router.register('comment', CommentListView)
router.register('rating', RatingListView)


urlpatterns = [
    path('', include(router.urls)),
    path('fav/', FavListView.as_view()),
    path('top/', TopListView.as_view()),
]
