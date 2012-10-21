from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.defaults import *

from moderation.helpers import auto_discover
from profiles.forms import UserProfileCustomForm, SignupFormExtra
from userena import views as userena_views

# below : kind of 'autodiscover' to associate ad filterset class to ad model class
# it's a bit tricky, and we would better do a register function for that
from sites.achetersanscom.ads.filtersets import HomeForSaleAdFilterSet
from sites.louersanscom.ads.filtersets import HomeForRentAdFilterSet


admin.autodiscover()
auto_discover()

urlpatterns = patterns('',
    url(r'^accounts/(?P<username>[\.\w]+)/edit/$',
        userena_views.profile_edit,
        {'template_name': 'userena/profile_form.html', 'edit_profile_form': UserProfileCustomForm},
        name='userena_profile_edit'),
    url(r'^accounts/signup/', userena_views.signup, {'signup_form': SignupFormExtra}),
    url(r'^accounts/', include('userena.urls')),
    url(r'^admin/', include(admin.site.urls)),
)


if settings.DEBUG == True:
    urlpatterns += (url(r'^media/(?P<path>.*)$',
        'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),)
