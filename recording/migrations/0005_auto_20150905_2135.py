# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recording', '0004_auto_20150905_2012'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='comment',
        ),
        migrations.AddField(
            model_name='comment',
            name='message',
            field=models.TextField(null=True, verbose_name=b'message', blank=True),
        ),
    ]
