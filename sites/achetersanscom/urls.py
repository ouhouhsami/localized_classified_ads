"""
achetersanscom urls.py

"""
from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import redirect_to

urlpatterns = patterns('',
    ('^$', redirect_to, {'url': '/annonce/search/'}),
    url(r'^annonce/', include('sites.achetersanscom.ads.urls')),
    url(r'^', include('localized_classified_ads.urls')),
)
