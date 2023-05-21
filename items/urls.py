from django.urls import path

from items.views import ItemsListView, favourite_item, item

app_name = 'items'

urlpatterns = [
    path('', ItemsListView.as_view(), name='index'),
    path('favourite_item/<slug:item_slug>/', favourite_item, name='favourite_item'),
    path('<slug:item_slug>/', item, name='item'),
]
