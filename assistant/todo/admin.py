from django.contrib import admin

from .models import Category, Files, Task


admin.site.register(Category)
admin.site.register(Files)
admin.site.register(Task)
