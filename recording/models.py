from django.db import models
from speaknow.models import Learner

class Recording(models.Model):
    learner = models.ForeignKey(Learner, on_delete='CASCADE')
    title = models.CharField(max_length=200, verbose_name='Title')
    audio = models.FileField(upload_to='audio/recording', verbose_name='Audio Upload')
    description = models.TextField(blank=True, null=True, verbose_name='Description')
    last_edited = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
        return self.title

class Comment(models.Model):
    learner = models.ForeignKey(Learner, on_delete='CASCADE', related_name='learner')
    recording = models.ForeignKey(Recording, on_delete='CASCADE', related_name='recording')
    message = models.TextField(blank=True, null=True, verbose_name='message')
    audio = models.FileField(upload_to='audio/comment', verbose_name='Audio Upload')
    last_edited = models.DateTimeField(null=True, blank=True)
