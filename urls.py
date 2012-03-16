from django.conf.urls.defaults import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from django.views.generic.simple import redirect_to
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib.sitemaps import FlatPageSitemap, GenericSitemap

from moderation.helpers import auto_discover
from profiles.forms import UserProfileCustomForm
from profiles.models import UserProfile
from userena import views as userena_views
from profiles.views import detail as profile_detail

#from ads.views import search

from sites.achetersanscom.ads.models import HomeForSaleAd
from sites.louersanscom.ads.models import HomeForRentAd

admin.autodiscover()
auto_discover()

home_for_sale_info_dict = {
    'queryset': HomeForSaleAd.objects.filter(visible=True),
    'date_field': 'create_date',
}
home_for_rent_info_dict = {
    'queryset': HomeForRentAd.objects.filter(visible=True),
    'date_field': 'create_date',
}

sitemaps = {
    'flatpages': FlatPageSitemap,
    'homeforsaleads': GenericSitemap(home_for_sale_info_dict, priority=0.6),
    'homeforrentads': GenericSitemap(home_for_rent_info_dict, priority=0.6),
}

#from sites.achetersanscom.ads.models import HomeForSaleAd, format_search_resume
#from sites.achetersanscom.ads.forms import HomeForSaleAdForm
#from sites.achetersanscom.ads.filtersets import HomeForSaleAdFilterSet

urlpatterns = patterns('',
    #line below is in specific site
    #url(r'^annonce/', include('ads.urls')),
    url(r'^accounts/(?P<username>(?!signout|signup|signin)[\.\w]+)/$',
       profile_detail, {},
       name='userena_profile_detail'),
    url(r'^accounts/(?P<username>[\.\w]+)/edit/$',
       userena_views.profile_edit, {'template_name':'userena/profile_form.html', 'edit_profile_form':UserProfileCustomForm},
       name='userena_profile_edit'),
    url(r'^accounts/', include('userena.urls')),
    #url(r'^$', search, name='search'),
    url(r'^admin/', include(admin.site.urls)),
    (r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
)

try:
    from settings_local import *
    # print 'local media donwload'
    urlpatterns += (url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root':settings.MEDIA_ROOT, 'show_indexes':True}),)
except ImportError:
    pass


