"""
louersanscom urls.py

"""
from django.conf.urls.defaults import patterns, include, url
from localized_classified_ads.ads.views import AdDetailView, AdCreateView, search, delete_search, add, CompleteView, view, AdDeleteView
from sites.louersanscom.ads.models import HomeForRentAd


urlpatterns = patterns('',
    url(r'^(?P<slug>[-\w]+)$', AdDetailView.as_view(model=HomeForRentAd), 
                                         name="view"),
    url(r'^search/(?P<search_id>\d+)$', search, name='search'),
    url(r'^delete_search/(?P<pk>\d+)$', AdSearchDeleteView.as_view(), 
                                         name='delete_search'),
    #url(r'^add/$', add, name='add'),
    url(r'^add/$', AdCreateView.as_view(model=HomeForRendAd), name='add'),
    url(r'^add/complete/$', CompleteView.as_view(), name='complete'),
    url(r'^(?P<ad_id>\d+)/edit$', edit, name='edit'),
    url(r'^(?P<ad_id>\d+)/delete$', AdDeleteView.as_view(model=HomeForRentAd), name='delete'),
)