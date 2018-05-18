from django.contrib import admin
from .models import Comment, Video, Post, Account

# Register your models here.
admin.site.register(Comment)
admin.site.register(Video)
admin.site.register(Post)
admin.site.register(Account)