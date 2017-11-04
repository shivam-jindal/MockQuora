# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MockQuora', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='question',
            old_name='topics',
            new_name='topic',
        ),
    ]
