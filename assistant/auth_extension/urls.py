from django.urls import path, re_path
from django.contrib.auth.views import (PasswordResetView, PasswordResetDoneView,
                                       PasswordResetConfirmView)

from . import views


urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('password_reset/', PasswordResetView.as_view(template_name='reset_password.html'),
         name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(template_name='reset_password_done.html'),
         name='password_reset_done'),
    re_path(r'^password_reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
            PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html',
                                             success_url='/'), name='password_reset_confirm')
]
