from django.conf.urls import url

from . import views

urlpatterns = [
    # ex: /recording/
    url(r'^$', views.IndexView.as_view(), name='index'),
    # ex: /recording/1/
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    # ex: /recording/create
    url(r'^create/$', views.CreateView.as_view(), name='create'),
    # ex: /recording/1/edit
    url(r'^(?P<pk>[0-9]+)/edit/$', views.EditView.as_view(), name='edit'),
    # ex: /recording/1/delete
    url(r'^(?P<pk>[0-9]+)/delete/$', views.DeleteView.as_view(), name='delete'),

]

