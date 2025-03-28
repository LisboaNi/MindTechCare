from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserModelViewSet
from . import views

router = DefaultRouter()
router.register(r'users', UserModelViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('', views.user_list, name='user_list'),
    path('create/', views.user_create, name='user_create'),
    path('update/<int:pk>/', views.user_update, name='user_update'),
    path('delete/<int:pk>/', views.user_delete, name='user_delete'),
]
