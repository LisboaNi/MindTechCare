# Generated by Django 5.1.7 on 2025-03-29 16:55

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_usermodel_cnpj'),
        ('employees', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel(
            old_name='User',
            new_name='Employee',
        ),
    ]
