from django.conf.urls.static import static
from django.conf import settings
from django.urls import path, re_path
from django.contrib.auth.views import (PasswordResetView, PasswordResetDoneView,
                                       PasswordResetConfirmView, LogoutView, LoginView)

from . import views


urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', LoginView.as_view(template_name='login.html',
                                     redirect_field_name='index'), name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('password_reset/', PasswordResetView.as_view(template_name='reset_password.html'),
         name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(template_name='reset_password_done.html'),
         name='password_reset_done'),
    re_path(r'^password_reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
            PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html',
                                             success_url='/', post_reset_login=True),
            name='password_reset_confirm'),
    path('user_profile/', views.profile_page, name='profile_page'),
    path('create_family/', views.create_family, name='create_family')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
