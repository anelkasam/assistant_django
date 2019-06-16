from django.conf.urls.static import static
from django.conf import settings
from django.urls import path

from . import views


urlpatterns = [
    path('tasks/', views.TaskList.as_view(), name='tasks'),
    path('tasks/<int:category_id>/', views.TaskList.as_view(), name='tasks_by_category'),
    path('task/add/', views.create_task, name='add_task'),
    path('category/add/', views.create_category, name='create_category'),
    path('edit/category/<int:cat_id>/', views.edit_category, name='edit_category'),
    path('edit/task/<int:task_id>/', views.edit_task, name='edit_task'),
    path('task/done/<int:task_id>/', views.done_task, name='done_task'),
    path('task/cancel/<int:task_id>/', views.cancel_task, name='cancel_task')

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
