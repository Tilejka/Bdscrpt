from django.shortcuts import HttpResponseRedirect, get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.views.generic.base import TemplateView, View
from django.views.generic.list import ListView

from hitcount.views import HitCountDetailView

from items.models import Item, ItemCategory, Quality, Comment
from items.forms import CommentForm


class IndexView(TemplateView):
    template_name = 'items/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data()
        context['title'] = 'Bdscrpt'
        return context


class ItemsListView(ListView):
    model = Item
    template_name = 'items/items.html'
    paginate_by = 3
    context_object_name = 'items'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ItemsListView, self).get_context_data()
        context['title'] = 'Beautiful Descriptions'
        context['categories'] = ItemCategory.objects.all()
        context['qualities'] = Quality.objects.all()
        filters = ''
        if 'favourites' in self.request.GET:
            filters = f'&favourites=True'
        if 'category' in self.request.GET:
            filters += ''.join([f'&category={x}' for x in self.request.GET.getlist('category')])
        if 'quality' in self.request.GET:
            filters += ''.join([f'&quality={x}' for x in self.request.GET.getlist('quality')])
        if 'keywords' in self.request.GET:
            filters += f'&keywords={self.request.GET["keywords"]}'
        context['filters'] = filters
        return context

    def get_queryset(self):
        queryset = super(ItemsListView, self).get_queryset()
        print(self.request.GET)
        if 'favourites' in self.request.GET:
            user = self.request.user
            queryset = user.favourite.all()
        if 'category' in self.request.GET:
            queryset = queryset.filter(category__slug__in=self.request.GET.getlist('category'))
        if 'keywords' in self.request.GET:
            queryset = queryset.filter(description__icontains=self.request.GET['keywords'])
        if 'quality' in self.request.GET:
            queryset = queryset.filter(quality__slug__in=self.request.GET.getlist('quality'))
        return queryset.order_by('name')


# def item(request, item_slug):
#     item = get_object_or_404(Item, slug=item_slug)
#
#     context = {
#         'title': item.name,
#         'item': item
#     }
#
#     return render(request, 'items/item.html', context=context)


class ItemDetailView(HitCountDetailView):
    model = Item
    template_name = 'items/item.html'
    slug_field = 'slug'
    count_hit = True

    form = CommentForm

    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        if form.is_valid():
            post = self.get_object()
            form.instance.user = request.user
            form.instance.post = post
            form.save()

            return redirect(reverse('items:item', kwargs={
                'slug': post.slug
            }))

    def get_context_data(self, **kwargs):
        post_comments_count = Comment.objects.all().filter(post=self.object.id).count()
        post_comments = Comment.objects.all().filter(post=self.object.id)
        context = super().get_context_data(**kwargs)
        context.update({
            'form': self.form,
            'post_comments': post_comments,
            'post_comments_count': post_comments_count,
        })
        return context


@login_required
def favourite_item(request, item_slug):
    item = get_object_or_404(Item, slug=item_slug)
    if item.favourite.filter(id=request.user.id).exists():
        item.favourite.remove(request.user)
    else:
        item.favourite.add(request.user)

    return HttpResponseRedirect(request.META['HTTP_REFERER'])
