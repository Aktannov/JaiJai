from django.contrib import admin

from video.models import Genre, Video, Anime, Rating

admin.site.register(Genre)
admin.site.register(Anime)
admin.site.register(Video)
admin.site.register(Rating)

