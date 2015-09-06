from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

# Register your models here.

from .models import Recording, Comment
from speaknow.models import User, Learner
from .models import Recording, Comment


class LearnerInline(admin.StackedInline):
    model = Learner
    can_delete = False

# Define a new User admin
class UserAdmin(UserAdmin):
    inlines = (LearnerInline,)

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Recording)
admin.site.register(Comment)


