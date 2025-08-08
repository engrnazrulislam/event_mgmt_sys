from django.urls import path
from users.views import sign_up, sign_in, sign_out, activate_user, admin_dashboard, assigned_role, create_group, group_list
from users.views import ProfileView, EditProfileView, ChangePassword, CustomPasswordResetView, CustomPasswordResetConfirmView
from django.contrib.auth.views import PasswordChangeDoneView
urlpatterns = [
    path('sign_up/',sign_up, name ='sign_up'),
    path('sign_in/',sign_in, name ='sign_in'),
    path('sign_out/',sign_out,name='sign_out'),
    path('activate/<int:user_id>/<str:token>/', activate_user),
    path('admin/dashboard/', admin_dashboard, name = 'admin_dashboard'),
    path('admin/<int:user_id>/assigned_role/',assigned_role, name='assigned_role'),
    path('admin/create_group/',create_group, name = 'create_group'),
    path('admin/group_list/', group_list, name = 'group_list'),
    path('profile/',ProfileView.as_view(), name='profile'),
    path('edit_profile/', EditProfileView.as_view(), name='edit_profile'),
    path('password_change/',ChangePassword.as_view(), name='password_change'),
    path('password_change/done/',PasswordChangeDoneView.as_view(template_name='accounts/password_change_done.html'), name='password_change_done'),
    path('password_reset/',CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/confirm/<uidb64>/<token>',CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
]
