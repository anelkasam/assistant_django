from django.conf.urls.static import static
from django.conf import settings
from django.urls import path

from . import views


urlpatterns = [
    path('tasks/', views.TaskList.as_view(), name='tasks'),
    path('category/<int:category_id>/', views.TaskList.as_view(), name='tasks_by_category'),
    path('task/add/', views.create_task, name='add_task')

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
