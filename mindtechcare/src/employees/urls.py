# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EmployeeViewSet
from . import views

router = DefaultRouter()
router.register(r'employees', EmployeeViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('employees/', views.employee_list, name='employee_list'),
    path('employee/profile/', views.employee_profile, name='employee_profile'),
    path('employee/create/', views.employee_create, name='employee-create'),
    path('employee/edit/<int:id>/', views.employee_edit, name='employee-edit'),
    path('employee/delete/<int:id>/', views.employee_delete, name='employee-delete'),
    path("employee/login/", views.employee_login, name="employee_login"),
    path("employee/logout/", views.employee_logout, name="employee_logout"),
]
