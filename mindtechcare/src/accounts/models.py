from django.db import models
from django.contrib.auth.models import User
from utils.models import TimestampMixin
from validations.validators import validate_cnpj, encrypt_password

class UserModel(TimestampMixin):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=255)
    cnpj = models.CharField(max_length=18, unique=True, db_index=True, validators=[validate_cnpj])
    email = models.EmailField(unique=True, null=True)
    password = models.CharField(max_length=255, null=True)

    def __str__(self):
        return f"{self.name}"
    
    def save(self, *args, **kwargs):
        if not self.id:
            user = User.objects.create_user(username=self.email, email=self.email, password=self.password)
            self.user = user

        if self.password:
            self.password = encrypt_password(self.password)

        super(UserModel, self).save(*args, **kwargs)
