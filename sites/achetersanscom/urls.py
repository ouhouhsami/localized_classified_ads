"""
achetersanscom urls.py

"""
from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    url(r'^annonce/', include('sites.achetersanscom.ads.urls')),
    url(r'^', include('localized_classified_ads.urls')),
)
