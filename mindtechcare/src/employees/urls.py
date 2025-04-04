from django.urls import path
from .views import (
    EmployeeLoginView,
    EmployeeLogoutView,
    EmployeeProfileView,
    EmployeeCreateView,
    EmployeeListView,
    EmployeeEditView,
    EmployeeDeleteView,
)

urlpatterns = [
    path('employee/login/', EmployeeLoginView.as_view(), name='employee_login'),
    path('employee/logout/', EmployeeLogoutView.as_view(), name='employee_logout'),
    path('employee/profile/', EmployeeProfileView.as_view(), name='employee_profile'),
    path('employee/create/', EmployeeCreateView.as_view(), name='employee_create'),
    path('employee/list/', EmployeeListView.as_view(), name='employee_list'),
    path('employee/edit/<int:pk>/', EmployeeEditView.as_view(), name='employee_edit'),
    path('employee/delete/<int:pk>/', EmployeeDeleteView.as_view(), name='employee_delete'),
]
