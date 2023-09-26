from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.contrib.contenttypes.models import ContentType

from .models import Comment


# @admin.register(Comment)
# class CommentAdmin(admin.ModelAdmin):
#     list_display = ('user', 'content_object', 'created_at')
#     list_filter = ('created_at', 'content_type')
#     search_fields = ('user__username', 'content')


def get_generic_foreign_key_filter(title, parameter_name=u'', separator='-', content_type_id_field='content_type_id', object_id_field='object_id') :

    class GenericForeignKeyFilter(SimpleListFilter):

        def __init__(self, request, params, model, model_admin):
            self.separator = separator
            self.title = title
            self.parameter_name = u'generic_foreign_key_' + parameter_name
            super(GenericForeignKeyFilter, self).__init__(request, params, model, model_admin)

        def lookups(self, request, model_admin):
            filter = object_id_field + '__isnull'  # for fields with null=True
            qs = model_admin.model.objects.all().order_by(content_type_id_field, object_id_field) .values_list(content_type_id_field, object_id_field).distinct()
            return [
                (
                    '{1}{0.separator}{2}'.format(self, *content_type_and_obj_id_pair),
                    ContentType.objects
                        .get(id=content_type_and_obj_id_pair[0])
                        .model_class()
                        .objects.get(pk=content_type_and_obj_id_pair[1])
                        .__str__()
                )
                for content_type_and_obj_id_pair
                in qs
            ]

        def queryset(self, request, queryset):
            try:
                content_type_id, object_id = self.value().split(self.separator)
                return queryset.filter(**({
                    content_type_id_field:content_type_id,
                    object_id_field:object_id
                }))
            except:
                return queryset

    return GenericForeignKeyFilter


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_filter = (get_generic_foreign_key_filter(u'Filter title'),)
    list_display = ('user', 'text', 'created_at')
    search_fields = ('text',)
    raw_id_fields = ('user',)
    readonly_fields = ('user', 'content_type', 'object_id', 'content_object', 'created_at')
    fields = readonly_fields + ('text',)
