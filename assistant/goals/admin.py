from django.contrib import admin

from goals.models import Goal
from notes.admin import NoteInline, LinkInline


class GoalAdmin(admin.ModelAdmin):
    inlines = [
        NoteInline,
        LinkInline,
    ]


admin.site.register(Goal, GoalAdmin)
