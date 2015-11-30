from django import forms
from django.template.defaultfilters import slugify

import os

from .models import Recording

'''
class UnicodeFileField(forms.FileField):

    def __init__(self, *args, **kwargs):
        super (UnicodeFileField, self).__init__(*args, **kwargs)

    def clean(self, *args, **kwargs):
        data = super(UnicodeFileField, self).clean(*args, **kwargs)
        #print data.name.encode('utf8')
        #data.name = unicode(data.name)

        #data.name = data.name.encode('utf8')
        #data.name = data.name.encode('ascii','ignore')
        if not all(ord(c) < 128 for c in data.name):
            raise forms.ValidationError(
                "The system currently does not support non-latin characters in the file name. "
                "Sorry for the inconvenience."
            )
        #print data

        #print data.name + u'.'+ slugify(filename[1])
        #if len(filename[1]):
         #   data.name += u'.'+slugify(filename[1])
        return data
'''

class UnicodeUploadForm(forms.ModelForm):
    class Meta:
        model = Recording
        #fields = ['title', 'language', 'audio', 'description']
        fields = ['title', 'language', 'description']

    #title = forms.CharField(label='Title', max_length=200, required=True)
    #audio = UnicodeFileField(label='Audio Upload', required=True)
    #description = forms.CharField(widget=forms.Textarea, required=False)

    # def clean_audio(self):
    #     data = self.cleaned_data['audio']
    #     if not all(ord(c) < 128 for c in data.name):
    #         raise forms.ValidationError(
    #             "The system currently does not support non-latin characters in the file name. "
    #             "Sorry for the inconvenience."
    #         )
    #     return data

    # def __init__(self, *args, **kwargs):
    #     self.request = kwargs.pop('request', None)
    #     super(UnicodeUploadForm, self).__init__(*args, **kwargs)
    #
    # def clean(self):


class CommentForm(forms.Form):
    message = forms.CharField(widget=forms.Textarea, required=False, label='Message')
    audio = forms.FileField(required=False, label='Audio')

    def clean(self):
        cleaned_data = super(CommentForm, self).clean()
        message = cleaned_data.get("message")
        audio = cleaned_data.get("audio")

        if not (message or audio):
            # If both fields are missing
            raise forms.ValidationError(
                "Please fill in either message or audio if not both."
            )