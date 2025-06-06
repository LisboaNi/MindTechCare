# Generated by Django 5.2 on 2025-04-14 11:26

import accounts.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0005_remove_usermodel_profile_picture"),
    ]

    operations = [
        migrations.AddField(
            model_name="usermodel",
            name="profile_image",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to=accounts.models.user_directory_path,
                verbose_name="Imagem de Perfil",
            ),
        ),
    ]
