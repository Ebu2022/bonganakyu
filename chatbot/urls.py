from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [

    # Authentication
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("change-password/", views.change_password, name="change_password"),

    # Chat interface
    path("chat/", views.chat_page, name="chat_page"),

    # API
    path("api/chat/", views.chat_api, name="chat_api"),

    # Password reset
    path(
        "forgot-password/",
        auth_views.PasswordResetView.as_view(
            template_name="chatbot/forgot_password.html",
            success_url="/password-reset-done/",
        ),
        name="password_reset",
    ),

    path(
        "password-reset-done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="chatbot/password_reset_done.html"
        ),
        name="password_reset_done",
    ),

    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="chatbot/password_reset_confirm.html"
        ),
        name="password_reset_confirm",
    ),

    path(
        "reset-complete/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="chatbot/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
]
