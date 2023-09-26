from django.urls import path
from comments.views import create_comment, delete_comment

app_name = 'comments'

urlpatterns = [
    path('create_comment/', create_comment, name='comment_create'),
    path('delete_comment/<int:comment_id>/', delete_comment, name='delete_comment'),
]
