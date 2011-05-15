from django.conf.urls.defaults import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from django.views.generic.simple import redirect_to
from django.core.urlresolvers import reverse
from moderation.helpers import auto_discover
from profiles.forms import UserProfileCustomForm
from profiles.models import UserProfile
from django.shortcuts import redirect
from django.conf import settings
from ads.views import search

admin.autodiscover()
auto_discover()

def redirect_login_user(request):
    return redirect('profile_detail', username=request.user.username)

urlpatterns = patterns('',
    url(r'^ads/', include('ads.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('userena.urls')),
    url(r'^profile/(?P<username>[\w\._-]+)/$', "profiles.views.detail", name="profile_detail"),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root':settings.MEDIA_ROOT, 'show_indexes':True}),
    #('^$', redirect_to, {'url': '/ads/search/'}),
    url(r'^$', search, name='search')
)

# urlpatterns += staticfiles_urlpatterns()

