# Generated by Django 4.2.1 on 2023-06-16 07:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0022_rename_catergory_post_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='avatar',
            field=models.ImageField(default='network/network/images/default.jpeg', upload_to='network/network/images'),
        ),
    ]
