# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ingest', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='content',
            name='content_name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='contentmetadata',
            name='meta_tags',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='upload',
            name='uploaded_file',
            field=models.FileField(upload_to='C:\\Users\\lami\\archiva\\archiva\\uploads/'),
        ),
    ]
