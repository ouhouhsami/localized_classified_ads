"""
louersanscom urls.py

"""
from django.conf.urls.defaults import patterns, include, url
from geoads.views import AdDetailView, AdSearchView, AdSearchDeleteView, AdUpdateView, AdCreateView, CompleteView, AdDeleteView

from sites.louersanscom.ads.models import HomeForRentAd
from sites.louersanscom.ads.forms import HomeForRentAdForm
from sites.louersanscom.ads.filtersets import HomeForRentAdFilterSet


urlpatterns = patterns('',
    url(r'^(?P<slug>[-\w]+)$', AdDetailView.as_view(model=HomeForRentAd), 
                                                            name="view"),
    url(r'^search/$', AdSearchView.as_view(model=HomeForRentAd, 
                                         filterset_class=HomeForRentAdFilterSet), 
                                                                  name='search'), 
    url(r'^search/(?P<search_id>\d+)/$', AdSearchView.as_view(model=HomeForRentAd, 
                                         filterset_class=HomeForRentAdFilterSet), 
                                                                  name='search'),
    url(r'^delete_search/(?P<pk>\d+)$', AdSearchDeleteView.as_view(), 
                                         name='delete_search'),
    url(r'^add/$', AdCreateView.as_view(model=HomeForRentAd, 
                                        form_class=HomeForRentAdForm), 
                                                             name='add'),
    url(r'^add/complete/$', CompleteView.as_view(), name='complete'),
    url(r'^(?P<pk>\d+)/edit$', AdUpdateView.as_view(model=HomeForRentAd, 
                                        form_class=HomeForRentAdForm), 
                                                            name='edit'),
    url(r'^(?P<pk>\d+)/delete$', AdDeleteView.as_view(model=HomeForRentAd), 
                                                          name='delete'),
)