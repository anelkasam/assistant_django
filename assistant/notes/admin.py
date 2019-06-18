from django import forms
from django.db import models
from django.contrib import admin
from django.forms import Textarea
from ckeditor.widgets import CKEditorWidget

from notes.models import Note, Link

class NoteAdminForm(forms.ModelForm):
    body = forms.CharField(widget=CKEditorWidget())
    widgets = {
        'text': forms.Textarea(attrs={'cols': 2, 'rows': 20}),
    }
    class Meta:
        model = Note
        fields = '__all__'

class NoteAdmin(admin.ModelAdmin):
    form = NoteAdminForm


class NoteInline(admin.TabularInline):
    model = Note
    extra = 0


class LinkInline(admin.TabularInline):
    model = Link
    extra = 0

admin.site.register(Note, NoteAdmin)
admin.site.register(Link)
