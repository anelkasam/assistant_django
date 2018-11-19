from django.conf.urls.static import static
from django.conf import settings
from django.urls import path

from . import views


urlpatterns = [
    path('', views.GoalList.as_view(), name='main_goals'),
    path('<int:pk>/', views.GoalDetailView.as_view(), name='goal_detail')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
