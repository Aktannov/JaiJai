from django.contrib import admin

from video.models import Genre, Video, Anime

admin.site.register(Genre)
admin.site.register(Anime)
admin.site.register(Video)

