# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()

urlpatterns = [
    path('api/', include(router.urls)),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
]