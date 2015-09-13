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

from .forms import UnicodeUploadForm, CommentForm
from .models import Recording, Comment


class IndexView(generic.ListView):
    template_name = 'recording/index.html'
    context_object_name = 'recording_list'

    def get_queryset(self):
        # This part will need to be modified in MVP -- all users can see public recordings, not just some with
        # permissions
        if self.request.user.has_perm('speaknow.see_all'):
            return Recording.objects.all().order_by('-last_edited')
        else:
            return Recording.objects.filter(learner=self.request.user.learner).order_by('-last_edited')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(IndexView, self).dispatch(*args, **kwargs)



'''
class CommentView(generic.detail.SingleObjectMixin, generic.FormView):
    template_name = 'recording/detail.html'
    form_class = CommentForm
    model = Comment

    def post(self, request, *args, **kwargs):
        print self.get_object()
        self.object = self.get_object()
        return super(CommentView, self).post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('recording-detail', kwargs={'pk': self.object.pk})

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(CommentView, self).dispatch(*args, **kwargs)
'''

class DetailView(generic.edit.FormMixin, generic.DetailView):
    model = Recording
    template_name = 'recording/detail.html'
    form_class = CommentForm

    def get_queryset(self):
        # This part will need to be modified in MVP -- all users can see public recordings, not just some with
        # permissions
        if self.request.user.has_perm('speaknow.see_all'):
            return Recording.objects.filter(pk=self.kwargs['pk'])
        else:
            return Recording.objects.filter(learner=self.request.user.learner, pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        recording = context['recording']
        context['comments'] = Comment.objects.filter(recording=recording).order_by('last_edited')
        context['form'] = self.get_form()
        context['learner'] = self.request.user.learner
        return context

    def get_success_url(self):
        return reverse('recording:detail', kwargs={'pk': self.object.pk})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        recording = context['recording']
        new_comment = Comment()
        new_comment.learner = self.request.user.learner
        new_comment.recording = recording #?
        new_comment.message = form.cleaned_data['message']
        new_comment.audio = form.cleaned_data['audio']
        new_comment.last_edited = timezone.now()
        new_comment.save()
        return super(DetailView, self).form_valid(form)

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

'''
class RecordingView(generic.View):
    def get(self, request, *args, **kwargs):
        view = DetailView.as_view()
        return view(request, *args, **kwargs)
    def post(self, request, *args, **kwargs):
        view = CommentView.as_view()
        return view(request, *args, **kwargs)
'''

class CreateView(generic.edit.CreateView):
    model = Recording
    #fields = ['title', 'audio', 'description']
    form_class = UnicodeUploadForm
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
    #fields = ['title', 'audio', 'description']
    form_class = UnicodeUploadForm
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

class DeleteComment(generic.edit.DeleteView):
    model = Comment
    template_name = 'recording/delete_comment.html'

    def get_success_url(self):
        return reverse('recording:detail', kwargs={'pk': self.object.recording.pk})

    def get_queryset(self):
        return Comment.objects.filter(learner=self.request.user.learner, pk=self.kwargs['pk'])

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        self.object = self.get_object()
        return super(DeleteComment, self).dispatch(*args, **kwargs)

