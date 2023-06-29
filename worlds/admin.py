from django.contrib import admin

from worlds.models import WorldType, DivineRank, Alignment, Domain, WorldGod, World


@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin):
    list_display = ('name', 'id')
    readonly_fields = ('id', )
    prepopulated_fields = {'slug': ('name', )}


@admin.register(Alignment)
class AlignmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'id')
    readonly_fields = ('id', )
    prepopulated_fields = {'slug': ('name', )}


@admin.register(DivineRank)
class DivineRankAdmin(admin.ModelAdmin):
    list_display = ('name', 'id')
    readonly_fields = ('id', )
    prepopulated_fields = {'slug': ('name', )}


@admin.register(WorldType)
class WorldTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'id')
    readonly_fields = ('id', )
    prepopulated_fields = {'slug': ('name', )}


@admin.register(WorldGod)
class WorldGodAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'alignment', 'domains', 'rank', 'symbol')
    readonly_fields = ('id', )
    prepopulated_fields = {'slug': ('name', )}


@admin.register(World)
class WorldAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'world_type', 'world_gods')
    readonly_fields = ('created_timestamp', 'id')
    fields = ('name', 'slug', 'description', ('world_type', 'world_gods'), 'fav_world', 'image', 'created_timestamp')
    search_fields = ('name', )
    ordering = ('name', )
    prepopulated_fields = {'slug': ('name', )}
