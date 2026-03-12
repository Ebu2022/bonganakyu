from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [

    path("", views.login_view, name="login"),

    path("chat/", views.chat_page, name="chat_page"),

    path("api/chat/", views.chat_api, name="chat_api"),

    path("logout/", views.logout_view, name="logout"),

    path("change-password/", views.change_password, name="change_password"),

    # Forgot password
    path(
        "forgot-password/",
        auth_views.PasswordResetView.as_view(
            template_name="chatbot/forgot_password.html"
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
