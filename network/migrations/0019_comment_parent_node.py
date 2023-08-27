# Generated by Django 4.2.1 on 2023-06-14 23:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0018_remove_comment_likes'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='parent_node',
            field=models.ForeignKey(blank=True, null=True, on_delete=models.SET('[DELETED]'), related_name='replies', to='network.comment'),
        ),
    ]
