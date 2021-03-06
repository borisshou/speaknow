"""helloevent URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.views.generic.base import RedirectView
from django.core.urlresolvers import reverse, reverse_lazy

from . import views


urlpatterns = [
    # ex: /
    url(r'^$', RedirectView.as_view(url=reverse_lazy('home'))),
    # ex: /home/
    #url(r'^home/$', views.index, name='home'),
    url(r'^home/$', RedirectView.as_view(url=reverse_lazy('recording:index')), name='home'),
    # ex: /recording/...
    url(r'^recording/', include('recording.urls', namespace='recording')),
    # ex: /admin/...
    url(r'^admin/', include(admin.site.urls)),

    # ex: /login/
    url(r'^login/$', views.SignUpView.as_view(), name='login'), # change the name login and SignUp etc.
    #url(r'^signin/$', auth_views.login, name='signin'), # Need to find a way to forbid GET request to this; only POST allowed
    url(r'^signin/$', views.signin_prevent_get, name='signin'), # only POST is allowed for this URL

    url(r'^logout/$', auth_views.logout, name='logout'),
    url(r'^password_change/$', auth_views.password_change, name='password_change'),
    url(r'^password_change/done/$', auth_views.password_change_done, name='password_change_done'),

    # Need to complete the password reset urls


    # Default authentication views
    ## ^login/$ [name='login']
    ## ^logout/$ [name='logout']
    ## ^password_change/$ [name='password_change']
    ## ^password_change/done/$ [name='password_change_done']
    ## ^password_reset/$ [name='password_reset']
    ## ^password_reset/done/$ [name='password_reset_done']
    ## ^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$ [name='password_reset_confirm']
    ## ^reset/done/$ [name='password_reset_complete']
    #url(r'^', include('django.contrib.auth.urls')),

    url(r'^profile/$', views.user_profile, name='profile'),


    # for access of .js files for recorder -- JavaScript Web Workers require that they be from the same origin, not Amazon S3 (a different origin)
    url(r'^recorder/recorderWorker.js$', views.find_js_recorderWorker),
    url(r'^recorder/mp3Worker.js$', views.find_js_mp3Worker)

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

admin.site.site_header = 'SpeakNow Admin'

