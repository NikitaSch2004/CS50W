# Generated by Django 4.2.5 on 2024-03-06 19:01

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0004_rename_created_at_follow_timestamp'),
    ]

    operations = [
        migrations.AddField(
            model_name='postare',
            name='likes',
            field=models.ManyToManyField(blank=True, default=0, related_name='liked_posts', to=settings.AUTH_USER_MODEL),
        ),
    ]
