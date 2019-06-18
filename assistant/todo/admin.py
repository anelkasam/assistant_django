from django.contrib import admin

from todo.models import Category, Files, Task, DEFAULT_CATEGORY
from notes.admin import NoteInline, LinkInline


class CategoryAdmin(admin.ModelAdmin):
    def delete_queryset(self, request, queryset):
        super(CategoryAdmin, self).delete_queryset(request, queryset.exclude(id=DEFAULT_CATEGORY))

    def delete_model(self, request, obj):
        if obj.id != DEFAULT_CATEGORY:
            super(CategoryAdmin, self).get_actions(request)


class TaskAdmin(admin.ModelAdmin):
    inlines = [
        NoteInline,
        LinkInline,
    ]


admin.site.register(Category, CategoryAdmin)
admin.site.register(Files)
admin.site.register(Task, TaskAdmin)
