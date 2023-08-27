# Generated by Django 4.2.1 on 2023-06-08 03:25

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0014_alter_post_likes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='post_ikers', to=settings.AUTH_USER_MODEL),
        ),
    ]
