from django.contrib import admin

from items.models import ItemCategory, Item, Quality


@admin.register(Item)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'quality', 'category', 'id')
    readonly_fields = ('created_timestamp', 'id')
    fields = ('name', 'slug', 'description', ('quality', 'category'), 'favourite', 'image', 'created_timestamp')
    filter_horizontal = ('favourite', )
    search_fields = ('name', )
    ordering = ('name', )
    prepopulated_fields = {'slug': ('name', )}


@admin.register(ItemCategory)
class ItemCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'id')
    readonly_fields = ('id', )
    prepopulated_fields = {'slug': ('name', )}


@admin.register(Quality)
class QualityAdmin(admin.ModelAdmin):
    list_display = ('name', 'id')
    readonly_fields = ('id', )
    prepopulated_fields = {'slug': ('name', )}
