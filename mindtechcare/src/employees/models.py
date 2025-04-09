from django.db import models
from django.contrib.auth.models import User
from utils.models import TimestampMixin
from validations.validators import encrypt_password, encrypt_token, decrypt_token
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
        # Criar um User apenas se um ainda não estiver associado e se o email e senha estiverem definidos
        if not self.user and self.email and self.password:
            user = User.objects.create_user(username=self.email, email=self.email, password=self.password)
            self.user = user
        # Atualizar o email do User se o email do Employee mudar
        elif self.user and self.email and self.user.email != self.email:
            self.user.email = self.email
            self.user.username = self.email # Importante atualizar o username também
            self.user.save()

        if self.password and not self.password.startswith('pbkdf2_sha256'):
            self.password = encrypt_password(self.password)

        # Criptografar tokens se estiverem presentes e não estiverem criptografados
        if self.trello_token and not self.trello_token.startswith('gAAAA'):
            self.trello_token = encrypt_token(self.trello_token)

        if self.github_token and not self.github_token.startswith('gAAAA'):
            self.github_token = encrypt_token(self.github_token)

        super().save(*args, **kwargs)

        # Garantir que 'accounts' esteja sempre associado após a criação do Employee
        if self.accounts is None and self.user:
            try:
                self.accounts = UserModel.objects.get(user=self.user)
                super().save(update_fields=['accounts']) # Salvar apenas o campo 'accounts' para evitar loops
            except UserModel.DoesNotExist:
                # Lidar com o caso em que o UserModel não existe para o User (pode ser um erro na lógica)
                pass

        elif self.accounts:
            self.accounts.save()