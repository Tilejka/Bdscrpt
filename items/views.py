from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import HttpResponseRedirect, get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.views.generic.base import TemplateView, View
from django.views.generic.list import ListView

from hitcount.views import HitCountDetailView

from items.models import Item, ItemCategory, Quality


class IndexView(TemplateView):
    template_name = 'items/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data()
        context['title'] = 'Bdscrpt'
        return context


class ItemsListView(ListView):
    model = Item
    template_name = 'items/items.html'
    paginate_by = 5
    context_object_name = 'items'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ItemsListView, self).get_context_data()
        context['title'] = 'Beautiful Descriptions / Items'
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


class ItemDetailView(HitCountDetailView):
    model = Item
    template_name = 'items/item.html'
    slug_field = 'slug'
    count_hit = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


    # model = Item
    # template_name = 'items/item.html'
    # slug_field = 'slug'
    # count_hit = True
    #
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     return context


@login_required
def favourite_item(request, item_slug):
    item = get_object_or_404(Item, slug=item_slug)
    if item.favourite.filter(id=request.user.id).exists():
        item.favourite.remove(request.user)
        messages.info(request, f'Item "{item.name}" removed from favourites.')
    else:
        item.favourite.add(request.user)
        messages.info(request, f'Item "{item.name}" added to favourites.')

    return redirect(request.META.get('HTTP_REFERER', '/'))
