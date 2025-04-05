# Generated by Django 5.1.7 on 2025-03-29 22:54

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('github', '0004_repositoriogithub_git_token'),
    ]

    operations = [
        migrations.AddField(
            model_name='atividadegithub',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='atividadegithub',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='repositoriogithub',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='repositoriogithub',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
