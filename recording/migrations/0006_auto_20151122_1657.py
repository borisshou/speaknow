# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recording', '0005_auto_20150905_2135'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='audio',
            field=models.FileField(upload_to=b'audio/comment', null=True, verbose_name=b'Audio Upload', blank=True),
        ),
    ]
