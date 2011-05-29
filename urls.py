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
from userena import views as userena_views
from profiles.views import detail as profile_detail

admin.autodiscover()
auto_discover()

'''
def redirect_login_user(request):
    return redirect('profile_detail', username=request.user.username)
'''


urlpatterns = patterns('',
    url(r'^ads/', include('ads.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/(?P<username>(?!signout|signup|signin)[\.\w]+)/$',
       profile_detail, {},
       name='userena_profile_detail'),
    url(r'^accounts/(?P<username>[\.\w]+)/edit/$',
       userena_views.profile_edit, {'template_name':'userena/profile_geo_form.html', 'edit_profile_form':UserProfileCustomForm},
       name='userena_profile_edit'),
    url(r'^accounts/', include('userena.urls')),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root':settings.MEDIA_ROOT, 'show_indexes':True}),
    url(r'^$', search, name='search')
)

# urlpatterns += staticfiles_urlpatterns()

