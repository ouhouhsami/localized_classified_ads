from django.conf.urls.defaults import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from django.views.generic.simple import redirect_to
from django.core.urlresolvers import reverse
from moderation.helpers import auto_discover
from profiles.forms import UserProfileCustomForm
from profiles.models import UserProfile
from django.shortcuts import redirect

admin.autodiscover()
auto_discover()
import settings

def redirect_login_user(request):
    return redirect('profile_detail', username=request.user.username)

urlpatterns = patterns('',
    url(r'^ads/', include('ads.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('userena.urls')),
    #url(r'^accounts/', include('registration.backends.default.urls')),
    #url(r'^profiles/$', "profiles.views.list", name="profile_list"),
    #url(r'^profiles/profile/$', redirect_login_user),
    #url(r'^profiles/edit/$', 'idios.views.profile_edit', {'form_class': UserProfileCustomForm}, name="profile_edit"),
    url(r'^profile/(?P<username>[\w\._-]+)/$', "profiles.views.detail", name="profile_detail"),
    #url(r'^profiles/', include("idios.urls")),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root':settings.MEDIA_ROOT, 'show_indexes':True}),
    ('^$', redirect_to, {'url': '/ads/search/'}),
)

# urlpatterns += staticfiles_urlpatterns()

