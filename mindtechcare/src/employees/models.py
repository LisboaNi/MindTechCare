from django.db import models
from django.contrib.auth.models import User
from utils.models import TimestampMixin
from validations.validators import encrypt_password
from accounts.models import UserModel

class Employee(TimestampMixin):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, related_name='employees')
    accounts = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='employee_accounts')  # Alterado para ForeignKey
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True, null=True)
    password = models.CharField(max_length=255, null=True)
    function = models.CharField(max_length=50, null=True)
    trello_username = models.CharField(max_length=255, null=True, blank=True)  
    trello_token = models.CharField(max_length=255, blank=True, null=True) 
    github_username = models.CharField(max_length=255, null=True, blank=True)
    github_token = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.name}"
    
    def save(self, *args, **kwargs):
        if not self.id:
            user = User.objects.create_user(username=self.email, email=self.email, password=self.password)
            self.user = user  

        if self.password:
            self.password = encrypt_password(self.password)

        super(Employee, self).save(*args, **kwargs)

        if self.accounts is None:  # Verificando se 'accounts' está vazio
            self.accounts = UserModel.objects.get(user=self.user)  # Atribui o UserModel associado ao User
            self.save()  # Salva novamente após atribuição

        if self.accounts:
            self.accounts.save()
