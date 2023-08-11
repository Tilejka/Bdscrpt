from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from items.views import IndexView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name='index'),
    path('items/', include('items.urls', namespace='items')),
    path('worlds/', include('worlds.urls', namespace='worlds')),
    path('users/', include('users.urls', namespace='users')),
    path('rating/', include('rating.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
