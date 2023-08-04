from urllib.parse import urlencode

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponseRedirect, QueryDict
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import ListView
from hitcount.views import HitCountDetailView

from worlds.forms import CommentForm
from worlds.models import WorldType, World, WorldGod, DivineRank, Domain, Alignment, WComment, Sphere


class WorldsListView(ListView):
    model = World
    template_name = 'worlds/worlds.html'
    paginate_by = 2
    context_object_name = 'worlds'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Beautiful Descriptions / Worlds'
        context['world_types'] = WorldType.objects.all()
        context['world_gods'] = WorldGod.objects.all()

        filters = ''

        if 'fav_world' in self.request.GET:
            filters += '&fav_world=True'

        if 'world_type' in self.request.GET:
            filters += ''.join([f'&world_type={x}' for x in self.request.GET.getlist('world_type')])

        if 'world_gods' in self.request.GET:
            filters += ''.join([f'&world_gods={x}' for x in self.request.GET.getlist('world_gods')])

        if 'keywords' in self.request.GET:
            filters += f'&keywords={self.request.GET["keywords"]}'

        context['filters'] = filters

        return context

    def get_queryset(self):
        queryset = super(WorldsListView, self).get_queryset()

        filters = Q()

        if 'fav_world' in self.request.GET:
            user = self.request.user
            filters &= Q(user__fav_world=user)

        if 'world_type' in self.request.GET:
            filters &= Q(world_type__slug__in=self.request.GET.getlist('world_type'))

        if 'world_gods' in self.request.GET:
            filters &= Q(world_gods__slug__in=self.request.GET.getlist('world_gods'))

        if 'keywords' in self.request.GET:
            filters &= Q(description__icontains=self.request.GET['keywords'])

        return queryset.filter(filters).order_by('name')


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

            return redirect(reverse('worlds:world', kwargs={
                'slug': post.slug
            }))

    def get_context_data(self, **kwargs):
        current_world = self.get_object()

        # Retrieve all worlds in the same sphere as the current world
        similar_worlds = World.objects.filter(sphere=current_world.sphere.id)

        post_comments_count = WComment.objects.all().filter(post=current_world.id).count()
        post_comments = WComment.objects.all().filter(post=current_world.id)

        context = super().get_context_data(**kwargs)
        context.update({
            'form': self.form,
            'post_comments': post_comments,
            'post_comments_count': post_comments_count,
            'similar_worlds': similar_worlds,
        })

        return context


class WorldGodDetailView(HitCountDetailView):
    model = WorldGod
    template_name = 'worlds/gods.html'
    slug_field = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Retrieve similar gods by sphere
        current_god = self.get_object()
        similar_gods = WorldGod.objects.filter(sphere=current_god.sphere)

        context.update({
            'similar_gods': similar_gods,
        })

        return context


@login_required
def fav_world(request, world_slug):
    world = get_object_or_404(World, slug=world_slug)
    if world.fav_world.filter(id=request.user.id).exists():
        world.fav_world.remove(request.user)
    else:
        world.fav_world.add(request.user)

    return HttpResponseRedirect(request.META['HTTP_REFERER'])
