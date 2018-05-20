from django.db import models

# Create your models here.


class Comment(models.Model):
    ucid = models.UUIDField(primary_key=True, editable=False)
    title = models.CharField(max_length=100)
    content = models.TextField(blank=True)
    owner_id = models.CharField(max_length=50)
    publish_time = models.DateTimeField(auto_now_add=True)


class Video(models.Model):
    uvid = models.UUIDField(primary_key=True, editable=False)
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


class Post(models.Model):
    upid = models.UUIDField(primary_key=True, editable=False)
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


class Account(models.Model):
    """
    這個是帳號, username ,password_sha256, name, intro
    """
    uuid = models.UUIDField(primary_key=True, editable=False)
    username = models.CharField(max_length=50)
    password_sha256 = models.CharField(max_length=64)
    name = models.CharField(max_length=20)
    intro = models.TextField(blank=True)
    silver_coin = models.DecimalField(
        max_digits=10, decimal_places=0, default=0)  # coin for donate
    gold_coin = models.DecimalField(
        max_digits=10, decimal_places=0, default=0)  # coin for exchang money
    online_time = models.DecimalField(
        max_digits=10, decimal_places=0, default=0)  # unit:second
    videos = models.ForeignKey(Video, null=True, blank=True)
    posts = models.ForeignKey(Post, null=True, blank=True)
