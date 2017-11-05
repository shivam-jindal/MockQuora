# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MockQuora', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vote',
            name='comment',
            field=models.ForeignKey(default=0, blank=True, to='MockQuora.Comment', null=True),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='vote',
            unique_together=set([('question', 'answer', 'comment', 'vote_by')]),
        ),
    ]
