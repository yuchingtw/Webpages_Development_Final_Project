import uuid
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.db import models

# Create your models here.

VIODEO_IMAGEFILE_PATH = "videoPhotos"
VIDEO_PATH = "videos"
POST_IMAGEFILE_PATH = "postPhotos"


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
    xmr_address = models.CharField(max_length=95)

    def __str__(self):
        return self.username


class Video(models.Model):
    uvid = models.UUIDField(
        primary_key=True, editable=False, default=uuid.uuid4)
    title = models.CharField(max_length=100)
    photo = models.ImageField(upload_to=VIODEO_IMAGEFILE_PATH)
    video_path = models.FileField(upload_to=VIDEO_PATH)
    content = models.TextField(blank=True)
    classify = models.CharField(max_length=20)
    click_times = models.DecimalField(
        max_digits=20, decimal_places=0, default=0)
    video_length = models.DecimalField(max_digits=20, decimal_places=0)
    publish_time = models.DateTimeField(auto_now_add=True)
    watched_time = models.DecimalField(
        max_digits=20, decimal_places=0, default=0)
    like = models.DecimalField(max_digits=20, decimal_places=0, default=0)
    dislike = models.DecimalField(max_digits=20, decimal_places=0, default=0)
    uploder = models.ForeignKey(Account)

    def __str__(self):
        return self.title


class Post(models.Model):
    upid = models.UUIDField(
        primary_key=True, editable=False, default=uuid.uuid4)
    title = models.CharField(max_length=100)
    content = models.TextField(blank=True)
    photo = models.ImageField(upload_to=POST_IMAGEFILE_PATH)
    classify = models.CharField(max_length=20)
    click_times = models.DecimalField(max_digits=20, decimal_places=0)
    publish_time = models.DateTimeField(auto_now_add=True)
    watched_time = models.DecimalField(max_digits=20, decimal_places=0)
    like = models.DecimalField(max_digits=20, decimal_places=0)
    dislike = models.DecimalField(max_digits=20, decimal_places=0)
    uploder = models.ForeignKey(Account)

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
