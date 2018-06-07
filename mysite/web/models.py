import uuid
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.db import models

# Create your models here.

IMAGEFILE_PATH = "videoPhotos"
VIDEO_PATH = "videos"


class Video(models.Model):
    uvid = models.UUIDField(
        primary_key=True, editable=False, default=uuid.uuid4)
    title = models.CharField(max_length=100)
    photo = models.ImageField(upload_to=IMAGEFILE_PATH)
    video_path = models.FileField(upload_to=VIDEO_PATH)
    content = models.TextField(blank=True)
    classify = models.CharField(max_length=20)
    click_times = models.DecimalField(
        max_digits=20, decimal_places=0, default=0)
    vidoe_length = models.DecimalField(max_digits=20, decimal_places=0)
    publish_time = models.DateTimeField(auto_now_add=True)
    watched_time = models.DecimalField(
        max_digits=20, decimal_places=0, default=0)
    like = models.DecimalField(max_digits=20, decimal_places=0, default=0)
    dislike = models.DecimalField(max_digits=20, decimal_places=0, default=0)

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

    def __str__(self):
        return self.title


class Comment(models.Model):
    ucid = models.UUIDField(
        primary_key=True, editable=False, default=uuid.uuid4)
    title = models.CharField(max_length=100)
    content = models.TextField(blank=True)
    publish_time = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post, null=True, blank=True)
    Video = models.ForeignKey(Video, null=True, blank=True)

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
    silver_coin = models.PositiveIntegerField(
        default=0)  # coin for donate
    gold_coin = models.PositiveIntegerField(
        default=0)  # coin for exchang money
    online_time = models.PositiveIntegerField(
        default=0)  # unit:second
    videos = models.ForeignKey(Video, null=True, blank=True)
    posts = models.ForeignKey(Post, null=True, blank=True)
    comments = models.ForeignKey(Comment, null=True, blank=True)

    def __str__(self):
        return self.username
