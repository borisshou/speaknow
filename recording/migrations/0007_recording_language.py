# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recording', '0006_auto_20151122_1657'),
    ]

    operations = [
        migrations.AddField(
            model_name='recording',
            name='language',
            field=models.CharField(max_length=30, null=True, verbose_name=b'Language'),
        ),
    ]
