# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-05-20 14:44
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('uuid', models.UUIDField(editable=False, primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=50)),
                ('password_sha256', models.CharField(max_length=64)),
                ('name', models.CharField(max_length=20)),
                ('intro', models.TextField(blank=True)),
                ('silver_coin', models.DecimalField(decimal_places=0, default=0, max_digits=10)),
                ('gold_coin', models.DecimalField(decimal_places=0, default=0, max_digits=10)),
                ('online_time', models.DecimalField(decimal_places=0, default=0, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('ucid', models.UUIDField(editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=100)),
                ('content', models.TextField(blank=True)),
                ('owner_id', models.CharField(max_length=50)),
                ('publish_time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('upid', models.UUIDField(editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=100)),
                ('content', models.TextField(blank=True)),
                ('classify', models.CharField(max_length=20)),
                ('click_times', models.DecimalField(decimal_places=0, max_digits=20)),
                ('publish_time', models.DateTimeField(auto_now_add=True)),
                ('watched_time', models.DecimalField(decimal_places=0, max_digits=20)),
                ('like', models.DecimalField(decimal_places=0, max_digits=20)),
                ('dislike', models.DecimalField(decimal_places=0, max_digits=20)),
                ('owner_id', models.CharField(max_length=50)),
                ('comments', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='web.Comment')),
            ],
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('uvid', models.UUIDField(editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=100)),
                ('content', models.TextField(blank=True)),
                ('classify', models.CharField(max_length=20)),
                ('click_times', models.DecimalField(decimal_places=0, max_digits=20)),
                ('vidoe_length', models.DecimalField(decimal_places=0, max_digits=20)),
                ('publish_time', models.DateTimeField(auto_now_add=True)),
                ('watched_time', models.DecimalField(decimal_places=0, max_digits=20)),
                ('like', models.DecimalField(decimal_places=0, max_digits=20)),
                ('dislike', models.DecimalField(decimal_places=0, max_digits=20)),
                ('owner_id', models.CharField(max_length=50)),
                ('comments', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='web.Comment')),
            ],
        ),
        migrations.AddField(
            model_name='account',
            name='posts',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='web.Post'),
        ),
        migrations.AddField(
            model_name='account',
            name='videos',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='web.Video'),
        ),
    ]