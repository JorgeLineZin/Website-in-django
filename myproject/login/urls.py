from django.urls import path
from . import views

urlpatterns = [
    path("", views.login_home, name="login"),
    path("register/", views.register_home, name="register"),
    path("logout/", views.logout_view, name="logout"),
]
