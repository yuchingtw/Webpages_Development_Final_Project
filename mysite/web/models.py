from django.db import models

# Create your models here.
class Comment(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField(blank=True)
    publish_time = models.DateTimeField(auto_now_add=True)

class Video(models.Model):
    vid = models.DecimalField(max_digits=20, decimal_places=0)
    title = models.CharField(max_length=100)
    content = models.TextField(blank=True)
    classify = models.CharField(max_length=20)
    click_times = models.DecimalField(max_digits=20, decimal_places=0)
    vidoe_length = models.DecimalField(max_digits=20, decimal_places=0)  
    publish_time = models.DateTimeField(auto_now_add=True)
    watched_time = models.DecimalField(max_digits=20, decimal_places=0)
    like = models.DecimalField(max_digits=20, decimal_places=0)
    dislike = models.DecimalField(max_digits=20, decimal_places=0)
    owner_id = models.CharField(max_length=20)  #Account username
    comments = models.ForeignKey(Comment)

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField(blank=True)
    classify = models.CharField(max_length=20)
    click_times = models.DecimalField(max_digits=20, decimal_places=0)
    publish_time = models.DateTimeField(auto_now_add=True)
    watched_time = models.DecimalField(max_digits=20, decimal_places=0)
    like = models.DecimalField(max_digits=20, decimal_places=0)
    dislike = models.DecimalField(max_digits=20, decimal_places=0)
    owner_id = models.CharField(max_length=20)  #Account username
    comments = models.ForeignKey(Comment)

class Account(models.Model):
    uid = models.DecimalField(max_digits=20, decimal_places=0)
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    name = models.CharField(max_length=20)
    intro = models.TextField(blank=True)
    silver_coin = models.DecimalField(max_digits=10, decimal_places=0)  #coin for donate
    gold_coin = models.DecimalField(max_digits=10, decimal_places=0)    #coin for exchang money
    online_time = models.DecimalField(max_digits=10, decimal_places=0)  #unit:second
    videos = models.ForeignKey(Video)
    posts = models.ForeignKey(Post)
