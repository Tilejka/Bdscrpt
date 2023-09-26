from django.urls import path

from worlds.views import WorldsListView, WorldDetailView, WorldGodDetailView, WorldGodsListView, fav_world

app_name = 'worlds'

urlpatterns = [
    path('', WorldsListView.as_view(), name='index'),
    path('gods/', WorldGodsListView.as_view(), name='gods'),
    path('fav_world/<slug:world_slug>/', fav_world, name='fav_world'),
    path('<slug>', WorldDetailView.as_view(), name='world'),
    path('gods/<slug>/', WorldGodDetailView.as_view(), name='gods'),
]
