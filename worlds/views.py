from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic import ListView

from hitcount.views import HitCountDetailView

from worlds.models import WorldType, World, WorldGod, Sphere, Alignment, Domain, DivineRank


class WorldsListView(ListView):
    model = World
    template_name = 'worlds/worlds.html'
    paginate_by = 5
    context_object_name = 'worlds'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(WorldsListView, self).get_context_data()
        context['title'] = 'Beautiful Descriptions / Worlds'
        context['world_types'] = WorldType.objects.all()
        context['world_gods'] = WorldGod.objects.all()
        context['world_sphere'] = Sphere.objects.all()

        full_path = self.request.get_full_path()
        print(full_path)

        filters = ''

        if 'fav_world' in self.request.GET:
            filters = f'&favourites=True'
        if 'world_type' in self.request.GET:
            filters += ''.join([f'&world_type={x}' for x in self.request.GET.getlist('world_type')])
        if 'world_gods' in self.request.GET:
            filters += ''.join([f'&world_gods={x}' for x in self.request.GET.getlist('world_gods')])
        if 'world_sphere' in self.request.GET:
            filters += ''.join([f'&world_sphere={x}' for x in self.request.GET.getlist('world_sphere')])
        if 'keywords' in self.request.GET:
            filters += f'&keywords={self.request.GET["keywords"]}'

        context['filters'] = filters

        return context

    def get_queryset(self):
        queryset = super(WorldsListView, self).get_queryset()
        if 'fav_world' in self.request.GET:
            user = self.request.user
            queryset = user.fav_world.all()
        if 'world_type' in self.request.GET:
            queryset = queryset.filter(world_type__slug__in=self.request.GET.getlist('world_type'))
        if 'world_gods' in self.request.GET:
            queryset = queryset.filter(world_gods__slug__in=self.request.GET.getlist('world_gods'))
        if 'world_sphere' in self.request.GET:
            queryset = queryset.filter(sphere__slug__in=self.request.GET.getlist('world_sphere'))
        if 'keywords' in self.request.GET:
            queryset = queryset.filter(description__icontains=self.request.GET['keywords'])
        return queryset.order_by('name').distinct()


class WorldDetailView(HitCountDetailView):
    model = World
    template_name = 'worlds/world.html'
    slug_field = 'slug'
    count_hit = True

    def get_context_data(self, **kwargs):
        current_world = self.get_object()

        # Retrieve all worlds in the same sphere as the current world
        similar_worlds = World.objects.filter(sphere=current_world.sphere.id)

        full_path = self.request.get_full_path()
        print(full_path)

        context = super().get_context_data(**kwargs)
        context.update({
            'similar_worlds': similar_worlds,
        })
        return context


class WorldGodsListView(ListView):
    model = WorldGod
    template_name = 'worlds/gods.html'
    paginate_by = 5
    context_object_name = 'gods'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(WorldGodsListView, self).get_context_data()
        context['title'] = 'Beautiful Descriptions / Worlds / Gods'
        context['alignment'] = Alignment.objects.all()
        context['divine_rank'] = DivineRank.objects.all()
        context['god_sphere'] = Sphere.objects.all()
        context['domain'] = Domain.objects.all()

        full_path = self.request.get_full_path()
        print(full_path)

        filters = ''

        # if 'fav_world' in self.request.GET:
        #     filters = f'&favourites=True'
        if 'alignment' in self.request.GET:
            filters += ''.join([f'&alignment={x}' for x in self.request.GET.getlist('alignment')])
        if 'rank' in self.request.GET:
            filters += ''.join([f'&rank={x}' for x in self.request.GET.getlist('rank')])
        if 'sphere' in self.request.GET:
            filters += ''.join([f'&sphere={x}' for x in self.request.GET.getlist('sphere')])
        if 'domain' in self.request.GET:
            filters += ''.join([f'&domain={x}' for x in self.request.GET.getlist('domain')])
        if 'keywords' in self.request.GET:
            filters += f'&keywords={self.request.GET["keywords"]}'

        context['filters'] = filters

        return context

    def get_queryset(self):
        queryset = super(WorldGodsListView, self).get_queryset()
        if 'fav_world' in self.request.GET:
            user = self.request.user
            queryset = user.fav_world.all()
        if 'alignment' in self.request.GET:
            queryset = queryset.filter(alignment__slug__in=self.request.GET.getlist('alignment'))
        if 'rank' in self.request.GET:
            queryset = queryset.filter(rank__slug__in=self.request.GET.getlist('rank'))
        if 'sphere' in self.request.GET:
            queryset = queryset.filter(sphere__slug__in=self.request.GET.getlist('sphere'))
        if 'domain' in self.request.GET:
            queryset = queryset.filter(domains__slug__in=self.request.GET.getlist('domain'))
        if 'keywords' in self.request.GET:
            queryset = queryset.filter(description__icontains=self.request.GET['keywords'])
        return queryset.order_by('name').distinct()


class WorldGodDetailView(HitCountDetailView):
    model = WorldGod
    template_name = 'worlds/god.html'
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
