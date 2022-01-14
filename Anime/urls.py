from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from Anime import settings
from django.conf.urls.static import static



schema_view = get_schema_view(
    openapi.Info(
        title='Test',
        default_version=1,
        description='Our internet shop',
    ),
    public=True,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('account.urls')),
    path('api/v1/', include('video.urls')),
    path('api/v1/docs/', schema_view.with_ui('swagger')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
