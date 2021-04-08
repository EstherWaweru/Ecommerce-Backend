#urls for accounts app

from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns=[
    path('signup/',views.signup,name='signup'),
    path('activate/<uidb64>/<token>/',views.activate,name='activate'),
    path('login/',views.user_login,name='user_login'),
    path('logout/',views.user_logout,name='user_logout'),
    path('password_reset/',auth_views.PasswordResetView.as_view(
        template_name='accounts/password_reset_form.html',
        subject_template_name='accounts/password_reset_subject.txt',
        email_template_name='accounts/password_reset_email.html',
         # success_url='/login/'
         ),name='password_reset'),
    path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(
        template_name='accounts/password_reset_done.html'
        ),name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(
        template_name='accounts/password_reset_confirm.html'
    ),name='password_reset_confirm'),
    path('password_reset/complete/',auth_views.PasswordResetCompleteView.as_view(
        template_name='accounts/password_reset_complete.html'
    ),name='password_reset_complete'),
    


]