from typing import Any
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from datetime import datetime
from django.core.exceptions import ValidationError

CATEGORY_CHOICES = [
    ('general', 'General Discussion'),
    ('help', 'Help and Support'),
    ('suggestions', 'Suggestions and Feedback'),
    ('introductions', 'Introductions'),
    ('offtopic', 'Off-Topic Discussion'),
    ('news', 'News and Announcements'),
    ('technology', 'Technology and Gadgets'),
    ('entertainment', 'Entertainment and Media'),
    ('sports', 'Sports and Fitness'),
    ('education', 'Education and Learning'),
    ('arts', 'Arts and Creativity'),
    ('food', 'Food and Cooking'),
    ('travel', 'Travel and Adventure'),
    ('music', 'Music and Audio'),
    ('movies', 'Movies and TV Shows'),
    ('books', 'Books and Literature'),
    ('fashion', 'Fashion and Style'),
    ('health', 'Health and Wellness'),
    ('politics', 'Politics and Current Events'),
    ('business', 'Business and Entrepreneurship'),
]

class User(AbstractUser):
    id = models.AutoField(primary_key=True)
    username = models.CharField(unique=True, max_length=26)
    avatar = models.ImageField(upload_to='network/images/', default='network/images/default.jpeg', unique=False)
    bio = models.CharField(max_length=350, default='Welcome to my account!')
    datetime_joined = models.DateTimeField(default=timezone.now)

class UserFollow(models.Model):
    user = models.ForeignKey('User', related_name="user", on_delete=models.CASCADE, verbose_name="User")
    is_now_following = models.ForeignKey('User', related_name="is_now_following", on_delete=models.CASCADE, verbose_name="User")
    datetime_followed = models.DateTimeField(default=timezone.now)

    def clean(self):
            if self.user == self.is_now_following:
                raise ValidationError("A user cannot follow themselves")
            
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'is_now_following'], name='unique-following-follower')
        ]

    def __str__(self):
        return f"{self.user} followed {self.is_now_following.username} at {self.datetime_followed}"

class Post(models.Model):
    post = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200, blank=False, null=False)
    text = models.CharField(max_length=2000, blank=False, null=False)
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name="post_poster")
    likes = models.ManyToManyField('User', blank=True, related_name="post_ikers")
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='general')
    upload_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
         return f"Post {self.post} uploaded by {self.user} at {self.upload_time}"

class Comment(models.Model):
    comment = models.AutoField(primary_key=True)
    text = models.CharField(max_length=250, blank=False, null=False)
    parent_node = models.ForeignKey('self', blank=True, null=True, on_delete=models.PROTECT, default=None, related_name='replies')
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name="comment_post")
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name="comment_poster")
    upload_time = models.DateTimeField(default=timezone.now)
