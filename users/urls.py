from django.urls import path
from users.views import sign_up, activate_user, admin_dashboard, assign_role, create_group, show_groups, CustomLogin, ProfileView, PasswordReset, PasswordResetConfirm, EditUserProfile, DeleteUser, PasswordChange
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('sign_up/',sign_up, name='sign-up'),
    path('sign_in/',CustomLogin.as_view(), name='sign-in'),
    path('sign_out/', LogoutView.as_view(), name="sign-out"),
    path('activate/<int:user_id>/<str:token>/', activate_user),
    path('admin-dashboard/', admin_dashboard, name="admin-dashboard"),
    path('admin/assign-role/<int:user_id>/', assign_role, name="assign-role"),
    path('admin/create-group/', create_group, name="create-group"),
    path('admin/show-groups/', show_groups, name="show-groups"),
    path('user-profile/', ProfileView.as_view(), name="user-profile"),
    path('change-password/', PasswordChange.as_view(), name="change-password"),
    path('password-reset/', PasswordReset.as_view(), name="password-reset"),
    path('password-reset/confirm/<uidb64>/<token>/', PasswordResetConfirm.as_view(), name="password_reset_confirm"),
    path('edit-profile/<int:user_id>/', EditUserProfile.as_view(), name="edit-profile"),
    path('delete-user/<int:user_id>', DeleteUser.as_view(), name="delete-user")
]