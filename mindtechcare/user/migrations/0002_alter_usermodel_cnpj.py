# Generated by Django 5.1.7 on 2025-03-28 02:49

import validations.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usermodel',
            name='cnpj',
            field=models.CharField(db_index=True, max_length=18, unique=True, validators=[validations.validators.validate_cnpj]),
        ),
    ]
