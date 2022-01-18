from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Genre(models.Model):
    name = models.CharField(max_length=30, unique=True)
    slug = models.SlugField(primary_key=True, blank=False)

    def __str__(self):
        return self.name


class Anime(models.Model):
    name = models.CharField(max_length=30, unique=True)
    slug = models.SlugField(primary_key=True)
    description = models.TextField()
    genre = models.ForeignKey(Genre, on_delete=models.RESTRICT, related_name='animes')
    image = models.ImageField(upload_to='animes')

    def __str__(self):
        return self.name, self.description


class Video(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='videos', blank=True, null=True)
    name = models.CharField(max_length=30)
    season = models.IntegerField()
    series = models.IntegerField()
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE, related_name='videos')
    video = models.FileField()


class Comment(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='comments', blank=True, null=True)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class Favorites(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='favorites', blank=True, null=True)
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE, related_name='favorites')


    class Meta:
        unique_together = ['anime', 'user']

    def __str__(self):
        return self.anime.name


class Likes(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='liked')
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='liked', blank=True, null=True)

    class Meta:
        unique_together = ['video', 'user']


class Rating(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='rating', blank=True, null=True)
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE, related_name='rating')
    rating = models.SmallIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ]
    )

    class Meta:
        unique_together = ['rating', 'user']

    def __str__(self):
        return f'{self.rating}'


# class Topp(models.Model):
#     text = models.TextField()
