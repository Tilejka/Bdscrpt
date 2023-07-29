from django.urls import path

from worlds.views import WorldsListView, WorldDetailView, WorldGodDetailView, fav_world

app_name = 'worlds'

urlpatterns = [
    path('', WorldsListView.as_view(), name='index'),
    path('fav_world/<slug:world_slug>/', fav_world, name='fav_world'),
    path('<slug>', WorldDetailView.as_view(), name='world'),
    path('gods/<slug>/', WorldGodDetailView.as_view(), name='gods'),
]
