# Generated by Django 4.2.1 on 2023-06-16 08:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0023_user_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(default='network/network/static/network/images/default.jpeg', upload_to='network/network/static/network/images/'),
        ),
    ]
