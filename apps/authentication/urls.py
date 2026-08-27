from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.login_page, name="login"),
    path("register/", views.register_page, name="register"),
    path("verify/", views.verify_page, name="verify"),
    path("forgot-password/", views.forgot_password_page, name="forgot_password"),
    path("change-password/", views.change_password_page, name="change_password"),
    path("security/", views.security_settings_page, name="security_settings"),
    path("logout/", views.logout_user, name="logout"),
]