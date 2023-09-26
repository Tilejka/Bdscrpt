from django import template
from django.contrib.contenttypes.models import ContentType
from comments.models import Comment

register = template.Library()


@register.inclusion_tag('comments/_comments.html')
def render_comments_for(obj, request):
    content_type = ContentType.objects.get_for_model(obj)
    comments = Comment.objects.filter(content_type=content_type, object_id=obj.id).order_by('-created_at')

    user = request.user
    is_staff = user.is_authenticated and user.is_staff

    return {
            'comments': comments,
            'is_staff': is_staff,
        }
