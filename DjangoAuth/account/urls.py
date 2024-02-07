from django.urls import path
from .views import *

urlpatterns = [
    path("register", UserRegistrationView.as_view(), name="register"),
    path("login", UserLoginView.as_view(), name="login"),
    path("profile", UserProfileView.as_view(), name="profile"),
    path("change-password", UserPasswordChangeView.as_view(), name="change-password"),
    path("send-reset-password-email", SendPasswordResetEmailView.as_view(), name="reset-password"),
    path("reset/<uid>/<token>", UserPasswordResetView.as_view(), name="reset-password"),

]
