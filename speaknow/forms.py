from django import forms
from .models import User, Client
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class UserForm(UserCreationForm):
    #password1 = forms.CharField(widget=forms.PasswordInput, min_length=6, label='Password', required=True)
    #password2 = forms.CharField(widget=forms.PasswordInput, min_length=6, label='Confirm Password', required=True)
    company_name = forms.CharField(label='Company Name', required=True)
    company_email = forms.EmailField(label='Company Email', required=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

class UserProfileForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.client = kwargs.pop('client', None)
        super(UserProfileForm, self).__init__(*args, **kwargs)

        self.fields['username'] = forms.CharField(label='User Name', required=True, initial=self.client.username)
        self.fields['first_name'] = forms.CharField(label='First Name', required=False, initial=self.client.first_name)
        self.fields['last_name'] = forms.CharField(label='Last Name', required=False, initial=self.client.last_name)
        self.fields['email'] = forms.EmailField(label='Email', required=False, initial=self.client.email)
        self.fields['company_name'] = forms.CharField(label='Company Name', required=True, initial=self.client.company_name)
        self.fields['company_email'] = forms.EmailField(label='Company Email', required=True, initial=self.client.company_email)
