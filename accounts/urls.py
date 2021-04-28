#urls for accounts app

from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns=[
    path('signup/',views.signup,name='signup'),
    path('activate/<uidb64>/<token>/',views.activate,name='activate'),
    path('login/',views.user_login,name='user_login'),
    path('logout/',views.user_logout,name='user_logout'),
    path('roles/',views.roles,name='roles'),
    path('roles/<str:group_id>/',views.role_view,name='role_view'),
    path('role_view_ajax/',views.role_view_ajax,name='role_view_ajax'),
    path('create_group_ajax/',views.create_group_ajax,name="create_group_ajax"),
    path('create_role/',views.create_role,name="create_role"),
    path('edit_group_ajax/',views.edit_group_ajax,name="edit_group_ajax"),
    path('ajax_edit_role/',views.ajax_edit_role,name="ajax_edit_role"),
    path('delete_group_ajax/',views.delete_group_ajax,name="delete_group_ajax"),
    path('add_permission/',views.add_permission,name="add_permission"),
    path('permissions/',views.permissions_list,name="permissions_list"),
    path('delete_permission/',views.delete_permission_ajax,name="delete_permission_ajax"),
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