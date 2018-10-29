from django.contrib import admin

from .models import Category, Files, Task, DEFAULT_CATEGORY


class CategoryAdmin(admin.ModelAdmin):
    def delete_queryset(self, request, queryset):
        super(CategoryAdmin, self).delete_queryset(request, queryset.exclude(id=DEFAULT_CATEGORY))

    def delete_model(self, request, obj):
        if obj.id != DEFAULT_CATEGORY:
            super(CategoryAdmin, self).get_actions(request)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Files)
admin.site.register(Task)
