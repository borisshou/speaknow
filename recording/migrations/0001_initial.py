# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('speaknow', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('comment', models.TextField(null=True, verbose_name=b'Comment', blank=True)),
                ('audio', models.FileField(upload_to=b'audio/comment', verbose_name=b'Audio Upload')),
                ('learner', models.ForeignKey(related_name='learner', on_delete=b'CASCADE', to='speaknow.Learner')),
            ],
        ),
        migrations.CreateModel(
            name='Recording',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200, verbose_name=b'Title')),
                ('audio', models.FileField(upload_to=b'audio/recording', verbose_name=b'Audio Upload')),
                ('description', models.TextField(null=True, verbose_name=b'Description', blank=True)),
                ('learner', models.ForeignKey(to='speaknow.Learner', on_delete=b'CASCADE')),
            ],
        ),
        migrations.AddField(
            model_name='comment',
            name='recording',
            field=models.ForeignKey(related_name='recording', on_delete=b'CASCADE', to='recording.Recording'),
        ),
    ]
