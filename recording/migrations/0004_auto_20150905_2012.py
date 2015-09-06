# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recording', '0003_auto_20150903_1802'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='message',
        ),
        migrations.AddField(
            model_name='comment',
            name='comment',
            field=models.TextField(null=True, verbose_name=b'Comment', blank=True),
        ),
    ]
