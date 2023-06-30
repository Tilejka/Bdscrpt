from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import ListView
from hitcount.views import HitCountDetailView

from items.forms import CommentForm
from worlds.models import WorldType, World, WorldGod, DivineRank, Domain, Alignment, WComment


class WorldsListView(ListView):
    model = World
    template_name = 'worlds/worlds.html'
    paginate_by = 3
    context_object_name = 'worlds'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(WorldsListView, self).get_context_data()
        context['title'] = 'Beautiful Descriptions / Worlds'
        context['world_type'] = WorldType.objects.all()
        filters = ''
        if 'fav_world' in self.request.GET:
            filters = f'&favourites=True'
        if 'world_type' in self.request.GET:
            filters += ''.join([f'&category={x}' for x in self.request.GET.getlist('category')])
        if 'keywords' in self.request.GET:
            filters += f'&keywords={self.request.GET["keywords"]}'
        context['filters'] = filters
        return context

    def get_queryset(self):
        queryset = super(WorldsListView, self).get_queryset()
        print(self.request.GET)
        if 'fav_world' in self.request.GET:
            user = self.request.user
            queryset = user.favourite.all()
        if 'world_type' in self.request.GET:
            queryset = queryset.filter(category__slug__in=self.request.GET.getlist('category'))
        if 'keywords' in self.request.GET:
            queryset = queryset.filter(description__icontains=self.request.GET['keywords'])
        return queryset.order_by('name')


class WorldDetailView(HitCountDetailView):
    model = World
    template_name = 'worlds/world.html'
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
        post_comments_count = WComment.objects.all().filter(post=self.object.id).count()
        post_comments = WComment.objects.all().filter(post=self.object.id)
        context = super().get_context_data(**kwargs)
        context.update({
            'form': self.form,
            'post_comments': post_comments,
            'post_comments_count': post_comments_count,
        })
        return context


@login_required
def fav_world(request, world_slug):
    item = get_object_or_404(World, slug=world_slug)
    if item.fav_world.filter(id=request.user.id).exists():
        item.fav_world.remove(request.user)
    else:
        item.fav_world.add(request.user)

    return HttpResponseRedirect(request.META['HTTP_REFERER'])
