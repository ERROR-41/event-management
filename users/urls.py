from django.urls import path
from users.views import (
    sign_up,
    activate_user,
    admin_dashboard,
    assign_role,
    create_group,
    group_list,
    update_group,
    profile,
    CustomLoginView,
    ChangePassword,
    CustomPasswordResetView,
    CustomPasswordRestConfirmView
)
from django.contrib.auth.views import LogoutView, PasswordChangeDoneView

urlpatterns = [
    path("sign-up/", sign_up, name="sign_up"),
    path("sign-in/", CustomLoginView.as_view(), name="sign_in"),
    path("sign-out/", LogoutView.as_view(), name="sign_out"),
    path("profile/", profile, name="profile"),
    path("password-change/", ChangePassword.as_view(), name="password_change"),
    path(
        "password-change-done/",
        PasswordChangeDoneView.as_view(template_name="accounts/password_change_done.html"),
        name="password_change_done",
    ),
    path('password-reset/',CustomPasswordResetView.as_view(),name='password_reset'),
    path('password-reset/confirm/<uidb64>/<token>/',CustomPasswordRestConfirmView.as_view(),name='password_reset_confirm'),
    path("activate/<int:user_id>/<str:token>/", activate_user, name="activate"),
    path("admin/dashboard/", admin_dashboard, name="admin_dashboard"),
    path("assign-role/<int:user_id>/", assign_role, name="assign_role"),
    path("create-group/", create_group, name="create_group"),
    path("edit-group/<int:group_id>", update_group, name="update_group"),
    path("group-list/", group_list, name="group_list"),
]
