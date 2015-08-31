from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse, reverse_lazy
from .models import Client, User
from .forms import UserForm, UserProfileForm
from django.contrib import messages

from event.models import Event, Logo, AppSkin, NavBar, Button
from rest_framework import viewsets
from helloevent.serializers import UserSerializer, ClientSerializer, EventSerializer, LogoSerializer, AppSkinSerializer, NavBarSerializer, ButtonSerializer

@login_required
def index(request):
    return render(request, 'home.html')

class SignUpView(generic.edit.CreateView):
    model = Client
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
            new_user.first_name = form.cleaned_data['first_name']
            new_user.last_name = form.cleaned_data['last_name']
            new_user.email = form.cleaned_data['email']
            new_user.save()

            new_client = Client.objects.get(user=new_user)
            new_client.company_name = form.cleaned_data['company_name']
            new_client.company_email = form.cleaned_data['company_email']
            new_client.save()
            messages.success(self.request, "You have successfully signed up. Log in here.")
            return HttpResponseRedirect(reverse_lazy('login'))

    def form_invalid(self, form):
        return self.render_to_response(
            self.get_context_data(form=form))

@login_required
def user_profile(request):
    client = request.user.client
    if request.method == 'POST':
        form = UserProfileForm(request.POST, client=client)
        if form.is_valid():
            user = User.objects.get(pk=request.user.pk)
            client = Client.objects.get(user=user)
            user.username = form.cleaned_data.get('username')
            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            user.email = form.cleaned_data.get('email')
            client.company_name = form.cleaned_data.get('company_name')
            client.company_email = form.cleaned_data.get('company_email')
            user.save()
            client.save()
            messages.success(request, 'You have successfully updated your user profile.')
            return redirect(reverse('home'))
    else:
        form = UserProfileForm(client=client)
    return render(request, 'registration/user_profile.html', context={'form': form})


# JSON API

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

class ClientViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

class EventViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Event.objects.all()
    serializer_class = EventSerializer

class LogoViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Logo.objects.all()
    serializer_class = LogoSerializer

class AppSkinViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = AppSkin.objects.all()
    serializer_class = AppSkinSerializer

class NavBarViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = NavBar.objects.all()
    serializer_class = NavBarSerializer

class ButtonViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Button.objects.all()
    serializer_class = ButtonSerializer