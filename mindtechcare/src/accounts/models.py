from django.db import models
from django.contrib.auth.models import User
from utils.models import TimestampMixin
from validations.validators import validate_cnpj, encrypt_password
import os
from uuid import uuid4


def user_directory_path(instance, filename):
    ext = filename.split(".")[-1]
    filename = f"{uuid4()}.{ext}"
    return os.path.join('profile_images', filename)


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
    profile_image = models.ImageField(
        upload_to=user_directory_path,
        null=True,
        blank=True,
        verbose_name="Imagem de perfil",
    )

    def __str__(self):
        return f"{self.name}"

    def save(self, *args, **kwargs):
        if not self.id:
            user = User.objects.create_user(
                username=self.email, email=self.email, password=self.password
            )
            self.user = user

        if self.password:
            self.password = encrypt_password(self.password)

        super(UserModel, self).save(*args, **kwargs)
