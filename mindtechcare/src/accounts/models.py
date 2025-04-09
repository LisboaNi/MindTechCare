from django.db import models
from django.contrib.auth.models import User
from utils.models import TimestampMixin
from validations.validators import validate_cnpj, encrypt_password


class UserModel(TimestampMixin):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=255, verbose_name="Nome")
    cnpj = models.CharField(
        max_length=18,
        unique=True,
        db_index=True,
        validators=[validate_cnpj],
        verbose_name="CNPJ",
    )
    email = models.EmailField(unique=True, null=True)
    password = models.CharField(max_length=255, null=True, verbose_name="Senha")

    def __str__(self):
        return f"{self.name}"

    def save(self, *args, **kwargs):
        # Criar um User apenas se um ainda não estiver associado
        if not self.user and self.email and self.password:
            user = User.objects.create_user(
                username=self.email, email=self.email, password=self.password
            )
            self.user = user
        # Atualizar o email do User se o email do UserModel mudar
        elif self.user and self.email and self.user.email != self.email:
            self.user.email = self.email
            self.user.username = self.email # Importante atualizar o username também
            self.user.save()

        if self.password and not self.password.startswith('pbkdf2_sha256'):
            self.password = encrypt_password(self.password)

        super(UserModel, self).save(*args, **kwargs)
