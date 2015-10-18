from django import forms
from .models import User, Learner
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class UserForm(UserCreationForm):
    #email = forms.EmailField(label='Email', required=True)
    #native_language = forms.CharField(label='Native Language(s)', required=True)
    #language_of_study = forms.CharField(label='Language(s) of Study', required=True)

    class Meta:
        model = User
        #fields = ['username', 'email']
        fields = ['username',]

class UserProfileForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.learner = kwargs.pop('learner', None)
        super(UserProfileForm, self).__init__(*args, **kwargs)

        self.fields['username'] = forms.CharField(label='Username', required=True, initial=self.learner.user.username)
        #self.fields['first_name'] = forms.CharField(label='First Name', required=False, initial=self.learner.first_name)
        #self.fields['last_name'] = forms.CharField(label='Last Name', required=False, initial=self.learner.last_name)
        self.fields['email'] = forms.EmailField(label='Email', required=True, initial=self.learner.user.email)
        self.fields['native_language'] = forms.CharField(label='Native Language(s)', required=True, initial=self.learner.native_language)
        self.fields['language_of_study'] = forms.CharField(label='Language(s) of Study', required=True, initial=self.learner.language_of_study)
