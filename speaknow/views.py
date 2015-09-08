from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib import messages

from .models import Learner, User
from .forms import UserForm, UserProfileForm

@login_required
def index(request):
    return render(request, 'home.html')

class SignUpView(generic.edit.CreateView):
    model = Learner
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')
    form_class = UserForm

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
            new_user.email = form.cleaned_data['email']
            new_user.save()

            new_learner = Learner.objects.get(user=new_user)
            new_learner.native_language = form.cleaned_data['native_language']
            new_learner.language_of_study = form.cleaned_data['language_of_study']
            new_learner.save()
            messages.success(self.request, "You have successfully signed up. Log in here.")
            return HttpResponseRedirect(reverse_lazy('login'))

    def form_invalid(self, form):
        return self.render_to_response(
            self.get_context_data(form=form))

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

