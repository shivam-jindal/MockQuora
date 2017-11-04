# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MockQuora', '0002_auto_20171105_0141'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='image',
            field=models.ImageField(null=True, upload_to=b'MockQuora/static/MockQuora/images', blank=True),
            preserve_default=True,
        ),
    ]
