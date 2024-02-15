from django.contrib.auth import views as auth_views
from django.urls import path, re_path, include
from .views import (
    register_view,
    logout_view,
    login_view
)

urlpatterns = [
  
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),


    # Password Reset urls
    path('reset/', auth_views.PasswordResetView.as_view(
        template_name='accounts/register/password_reset.html',
        email_template_name='accounts/register/password_reset_email.html',
        subject_template_name='accounts/register/password_reset_subject.txt'), name='password_reset'),
    path('reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='accounts/register/password_reset_done.html'), name='password_reset_done'),
    path('register-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='accounts/register/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='accounts/register/password_reset_complete.html'), name='password_reset_complete'),
    path('settings/register/', auth_views.PasswordChangeView.as_view(
        template_name='accounts/register/password_change.html'), name='password_change'),
    path('settings/register/done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='accounts/register/password_change_done.html'), name='password_change_done'),
]
