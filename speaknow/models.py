from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class Learner(models.Model):
    class Meta:
        permissions = (
            ("see_all", "Can see all recordings"),
        )

    user = models.OneToOneField(User)
    native_language = models.CharField(max_length=200, null=False, blank=False)
    language_of_study = models.CharField(max_length=200, null=False, blank=False)

    def __unicode__(self):
        return self.user.username

def create_learner(sender, instance, created, **kwargs):
    if created:
        learner, created = Learner.objects.get_or_create(user=instance)

post_save.connect(create_learner, sender=User)



