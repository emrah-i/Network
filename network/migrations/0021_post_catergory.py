# Generated by Django 4.2.1 on 2023-06-15 17:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0020_alter_comment_parent_node'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='catergory',
            field=models.CharField(choices=[('general', 'General Discussion'), ('help', 'Help and Support'), ('suggestions', 'Suggestions and Feedback'), ('introductions', 'Introductions'), ('offtopic', 'Off-Topic Discussion'), ('news', 'News and Announcements'), ('technology', 'Technology and Gadgets'), ('entertainment', 'Entertainment and Media'), ('sports', 'Sports and Fitness'), ('education', 'Education and Learning'), ('arts', 'Arts and Creativity'), ('food', 'Food and Cooking'), ('travel', 'Travel and Adventure'), ('music', 'Music and Audio'), ('movies', 'Movies and TV Shows'), ('books', 'Books and Literature'), ('fashion', 'Fashion and Style'), ('health', 'Health and Wellness'), ('politics', 'Politics and Current Events'), ('business', 'Business and Entrepreneurship')], default='general', max_length=20),
        ),
    ]
