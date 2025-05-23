# Generated by Django 5.1.7 on 2025-03-29 17:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_usermodel_cnpj'),
        ('employees', '0002_rename_user_employee'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='accounts',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='employee_accounts', to='accounts.usermodel'),
        ),
    ]
