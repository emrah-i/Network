# Generated by Django 4.2.4 on 2023-08-28 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0043_alter_user_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(default='/network/images/default.jpeg', upload_to=''),
        ),
    ]
