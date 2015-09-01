from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.views import generic
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.forms.formsets import formset_factory
from django.db import IntegrityError, transaction
from django.contrib import messages
from django.utils import timezone

from .models import Recording, Comment


class IndexView(generic.ListView):
    template_name = 'recording/index.html'
    context_object_name = 'recording_list'

    def get_queryset(self):
        return Recording.objects.filter(learner=self.request.user.learner).order_by('-last_edited')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(IndexView, self).dispatch(*args, **kwargs)

class DetailView(generic.DetailView):
    model = Recording
    template_name = 'recording/detail.html'

    def get_queryset(self):
        return Recording.objects.filter(learner=self.request.user.learner, pk=self.kwargs['pk'])

    #def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        #context = super(DetailView, self).get_context_data(**kwargs)
        #event = context['event']
        # Add in a QuerySet of all the images
        #context['logos'] = Logo.objects.filter(event=event)
        #context['app_skins'] = AppSkin.objects.filter(event=event)
        #context['nav_bars'] = NavBar.objects.filter(event=event)
        #context['buttons'] = Button.objects.filter(event=event)
        #return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(DetailView, self).dispatch(*args, **kwargs)

class CreateView(generic.edit.CreateView):
    model = Recording
    fields = ['title', 'audio', 'description']
    template_name = 'recording/create.html'
    success_url = reverse_lazy('recording:index')

    def form_valid(self, form):
        form.instance.learner = self.request.user.learner
        form.instance.last_edited = timezone.now()
        return super(CreateView, self).form_valid(form)

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(CreateView, self).dispatch(*args, **kwargs)

class EditView(generic.edit.UpdateView):
    model = Recording
    fields = ['title', 'audio', 'description']
    template_name = 'recording/edit.html'
    success_url = reverse_lazy('recording:index')

    def form_valid(self, form):
        form.instance.last_edited = timezone.now()
        return super(EditView, self).form_valid(form)

    def get_queryset(self):
        return Recording.objects.filter(learner=self.request.user.learner, pk=self.kwargs['pk'])

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(EditView, self).dispatch(*args, **kwargs)

class DeleteView(generic.edit.DeleteView):
    model = Recording
    template_name = 'recording/delete.html'
    success_url = reverse_lazy('recording:index')

    def get_queryset(self):
        return Recording.objects.filter(learner=self.request.user.learner, pk=self.kwargs['pk'])

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(DeleteView, self).dispatch(*args, **kwargs)