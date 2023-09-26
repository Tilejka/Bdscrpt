from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from django.contrib.contenttypes.models import ContentType
from comments.forms import CommentForm
from comments.models import Comment


@login_required
def create_comment(request):

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            content_type_pk = form.cleaned_data.get('content_type')
            content_type = ContentType.objects.get(pk=content_type_pk)
            object_id = form.cleaned_data.get('object_id')
            content = form.cleaned_data.get('content')

            Comment.objects.create(
                user=request.user,
                content_type=content_type,
                object_id=object_id,
                text=content
            )

            referrer = request.META.get('HTTP_REFERER')
            return redirect(referrer)


@staff_member_required(login_url='user:login')
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    comment.delete()

    return redirect(request.META.get('HTTP_REFERER', '/'))
