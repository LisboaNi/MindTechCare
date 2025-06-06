# Generated by Django 5.1.7 on 2025-04-04 03:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0003_alter_employee_accounts'),
        ('trello', '0003_boardtrello_trello_token'),
    ]

    operations = [
        migrations.AddField(
            model_name='cardtrello',
            name='employee',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='card_trello', to='employees.employee'),
        ),
        migrations.DeleteModel(
            name='AtividadeTrello',
        ),
    ]
