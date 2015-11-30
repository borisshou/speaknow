from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotAllowed
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.contrib.staticfiles.templatetags.staticfiles import static
import requests

from .models import Learner, User
from .forms import UserForm, UserProfileForm

@login_required
def index(request):
    return render(request, 'home.html')

def signin_prevent_get(request): # to have two forms on one page - this url is forbidden when having GET request
    if request.method != 'POST':
        return HttpResponseNotAllowed('You cannot access this page')
    else:
        return auth_views.login(request) # Can only be used for POST when user logs in

class SignUpView(generic.edit.CreateView):
    model = Learner
    template_name = 'registration/login.html'
    success_url = reverse_lazy('login')
    form_class = UserForm

    def get_context_data(self, **kwargs):
        context = super(SignUpView, self).get_context_data(**kwargs)
        signup_form = context.pop('form') # differentiate between the forms on the main page
        context['signup_form'] = signup_form
        return context

    def post(self, request, *args, **kwargs):
        self.object = None
        form = UserForm(self.request.POST)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        username = form.cleaned_data['username']
        existing_users = User.objects.filter(username=username)
        if not existing_users:
            new_user = User()
            new_user.username = form.cleaned_data['username']
            new_user.set_password(form.cleaned_data['password1'])
            #new_user.first_name = form.cleaned_data['first_name']
            #new_user.last_name = form.cleaned_data['last_name']
            #new_user.email = form.cleaned_data['email']
            new_user.save()

            new_learner = Learner.objects.get(user=new_user)
            #new_learner.native_language = form.cleaned_data['native_language']
            #new_learner.language_of_study = form.cleaned_data['language_of_study']
            new_learner.save()
            messages.success(self.request, "You have successfully signed up.")
            return HttpResponseRedirect(self.success_url + '#features') # render the page at a specific position

    def form_invalid(self, form):
        context = self.get_context_data(form=form)
        context['go_to_features'] = True # Indicate to the page that it needs to be loaded with the section "features"
        # being displayed - the front end will do the work
        return self.render_to_response(context)

@login_required
def user_profile(request):
    learner = request.user.learner
    if request.method == 'POST':
        form = UserProfileForm(request.POST, learner=learner)
        if form.is_valid():
            user = User.objects.get(pk=request.user.pk)
            learner = Learner.objects.get(user=user)
            user.username = form.cleaned_data.get('username')
            #user.first_name = form.cleaned_data.get('first_name')
            #user.last_name = form.cleaned_data.get('last_name')
            user.email = form.cleaned_data.get('email')
            learner.native_language = form.cleaned_data.get('native_language')
            learner.language_of_study = form.cleaned_data.get('language_of_study')
            user.save()
            learner.save()
            messages.success(request, 'You have successfully updated your user profile.')
            return redirect(reverse('home'))
    else:
        form = UserProfileForm(learner=learner)
    return render(request, 'registration/user_profile.html', context={'form': form})




def find_js_recorderWorker(request):
    if settings.DEBUG: # local
        url = "http://" + request.get_host() + static('js/recorder/recorderWorker.js')
    else: # deployed
        url = static('js/recorder/recorderWorker.js') # will obtain an Amazon S3 storage address such as follows
        #url = 'https://speaknowapp.s3.amazonaws.com/static/js/recorder/recorderWorker.js?Signature=P%2Fz%2BpLnETvlyyf%2FJ9HtYRz0ljZA%3D&Expires=1448860345&AWSAccessKeyId=AKIAJVNNABYOMGHAVMJA'
    r = requests.get(url)
    return HttpResponse(r.text, content_type = "application/javascript")


def find_js_mp3Worker(request):
    if settings.DEBUG: # local
        url = "http://" + request.get_host() + static('js/recorder/mp3Worker.js')
    else: # deployed
        url = static('js/recorder/mp3Worker.js') # will obtain an Amazon S3 storage address such as follows
        #url = 'https://speaknowapp.s3.amazonaws.com/static/js/recorder/recorderWorker.js?Signature=P%2Fz%2BpLnETvlyyf%2FJ9HtYRz0ljZA%3D&Expires=1448860345&AWSAccessKeyId=AKIAJVNNABYOMGHAVMJA'
    r = requests.get(url)
    return HttpResponse(r.text, content_type = "application/javascript")