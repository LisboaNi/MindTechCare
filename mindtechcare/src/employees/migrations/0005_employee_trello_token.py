# Generated by Django 5.1.7 on 2025-04-05 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0004_employee_trello_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='trello_token',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
