# Generated by Django 4.2.1 on 2023-06-07 09:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0009_alter_user_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userfollow',
            name='is_now_following',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='is_now_following', to=settings.AUTH_USER_MODEL),
        ),
    ]
