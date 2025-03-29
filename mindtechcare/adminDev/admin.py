from django.contrib import admin
from accounts.models import UserModel
from employees.models import Employee

@admin.register(UserModel)
class UserModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email') 
    search_fields = ('name', 'email')

@admin.register(Employee)
class UserModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email') 
    search_fields = ('name', 'email')