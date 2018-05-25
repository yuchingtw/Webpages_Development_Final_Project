import uuid
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.db import models

# Create your models here.


class Comment(models.Model):
    ucid = models.UUIDField(
        primary_key=True, editable=False, default=uuid.uuid4)
    title = models.CharField(max_length=100)
    content = models.TextField(blank=True)
    owner_id = models.CharField(max_length=50)
    publish_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Video(models.Model):
    uvid = models.UUIDField(
        primary_key=True, editable=False, default=uuid.uuid4)
    title = models.CharField(max_length=100)
    content = models.TextField(blank=True)
    classify = models.CharField(max_length=20)
    click_times = models.DecimalField(max_digits=20, decimal_places=0)
    vidoe_length = models.DecimalField(max_digits=20, decimal_places=0)
    publish_time = models.DateTimeField(auto_now_add=True)
    watched_time = models.DecimalField(max_digits=20, decimal_places=0)
    like = models.DecimalField(max_digits=20, decimal_places=0)
    dislike = models.DecimalField(max_digits=20, decimal_places=0)
    owner_id = models.CharField(max_length=50)  # Account username
    comments = models.ForeignKey(Comment, null=True, blank=True)

    def __str__(self):
        return self.title


class Post(models.Model):
    upid = models.UUIDField(
        primary_key=True, editable=False, default=uuid.uuid4)
    title = models.CharField(max_length=100)
    content = models.TextField(blank=True)
    classify = models.CharField(max_length=20)
    click_times = models.DecimalField(max_digits=20, decimal_places=0)
    publish_time = models.DateTimeField(auto_now_add=True)
    watched_time = models.DecimalField(max_digits=20, decimal_places=0)
    like = models.DecimalField(max_digits=20, decimal_places=0)
    dislike = models.DecimalField(max_digits=20, decimal_places=0)
    owner_id = models.CharField(max_length=50)  # Account username
    comments = models.ForeignKey(Comment, null=True, blank=True)

    def __str__(self):
        return self.title


class Account(AbstractUser):
    """
    這個是帳號  nickname, intro, coin, videos, posts
    """

    class Meta():
        verbose_name = _('account')
        verbose_name_plural = _('accounts')

    nickname = models.CharField(max_length=20)
    intro = models.TextField(blank=True)
    silver_coin = models.DecimalField(
        max_digits=10, decimal_places=0, default=0)  # coin for donate
    gold_coin = models.DecimalField(
        max_digits=10, decimal_places=0, default=0)  # coin for exchang money
    online_time = models.DecimalField(
        max_digits=10, decimal_places=0, default=0)  # unit:second
    videos = models.ForeignKey(Video, null=True, blank=True)
    posts = models.ForeignKey(Post, null=True, blank=True)

    def __str__(self):
        return self.username
