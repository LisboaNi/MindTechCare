from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserModelViewSet
from . import views
from django.contrib.auth import views as auth_views

router = DefaultRouter()
router.register(r'users', UserModelViewSet)

urlpatterns = [

    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('api/', include(router.urls)),
    path('accounts/user_list/', views.user_list, name='user_list'),
    path('accounts/create/', views.user_create, name='user_create'),
    path('accounts/update/<int:pk>/', views.user_update, name='user_update'),
    path('accounts/delete/<int:pk>/', views.user_delete, name='user_delete'),
    path("accounts/login/", views.user_login, name="user_login"),
    path("accounts/logout/", views.user_logout, name="user_logout"),
    
]
