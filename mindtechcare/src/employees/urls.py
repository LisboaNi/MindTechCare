from django.urls import path
from .views import (
    EmployeeLoginView,
    EmployeeLogoutView,
    EmployeeProfileView,
    EmployeeCreateView,
    EmployeeListView,
    EmployeeEditView,
    EmployeeDeleteView,
    TokenUpdateView,
)

urlpatterns = [
    path('login/', EmployeeLoginView.as_view(), name='employee_login'),
    path('logout/', EmployeeLogoutView.as_view(), name='employee_logout'),
    path('profile/', EmployeeProfileView.as_view(), name='employee_profile'),
    path('create/', EmployeeCreateView.as_view(), name='employee_create'),
    path('list/', EmployeeListView.as_view(), name='employee_list'),
    path('edit/<int:pk>/', EmployeeEditView.as_view(), name='employee_edit'),
    path('delete/<int:pk>/', EmployeeDeleteView.as_view(), name='employee_delete'),

    path('token/', TokenUpdateView.as_view(), name='token_edit'),

]
