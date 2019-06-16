from django import forms
from django.contrib import admin
from ckeditor.widgets import CKEditorWidget

from notes.models import Note

class NoteAdminForm(forms.ModelForm):
    body = forms.CharField(widget=CKEditorWidget())
    class Meta:
        model = Note
        fields = '__all__'

class NoteAdmin(admin.ModelAdmin):
    form = NoteAdminForm

admin.site.register(Note, NoteAdmin)
