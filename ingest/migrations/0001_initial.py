# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import ingest.utils
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AccountLog',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('time_in', models.TimeField()),
                ('time_out', models.TimeField()),
                ('date', models.DateField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Content',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('content_name', models.CharField(max_length=30)),
                ('repo_name', models.CharField(max_length=30, null=True)),
                ('file', models.FileField(null=True, upload_to=ingest.utils.change_upload_path)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('user', models.OneToOneField(primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('interest', models.CharField(max_length=100, null=True)),
                ('occupation', models.CharField(max_length=30, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Repository',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=25)),
                ('repo_size', models.IntegerField(default=0)),
                ('date_created', models.DateTimeField(auto_now=True)),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Upload',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=40)),
                ('uploaded_file', models.FileField(upload_to=ingest.utils.change_upload_path)),
            ],
        ),
        migrations.CreateModel(
            name='ContentMetadata',
            fields=[
                ('content', models.OneToOneField(primary_key=True, serialize=False, to='ingest.Content')),
                ('file_type', models.CharField(max_length=20)),
                ('file_size', models.IntegerField(default=0)),
                ('date_uploaded', models.DateTimeField(auto_now=True)),
                ('meta_tags', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('permissions', models.TextField()),
            ],
        ),
        migrations.AddField(
            model_name='content',
            name='owner',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='content',
            name='repo',
            field=models.ForeignKey(null=True, to='ingest.Repository'),
        ),
        migrations.AddField(
            model_name='accountlog',
            name='acc_user',
            field=models.ForeignKey(null=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
