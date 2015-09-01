# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recording', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='last_edited',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='recording',
            name='last_edited',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
