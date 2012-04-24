"""
AcheterSansCom urls.py

"""
from django.conf.urls.defaults import patterns, include, url
from geoads.views import (AdSearchView, AdDetailView, 
                              AdSearchDeleteView, AdCreateView,  AdUpdateView, 
                              CompleteView, AdDeleteView)
from sites.achetersanscom.ads.models import HomeForSaleAd 
from sites.achetersanscom.ads.forms import HomeForSaleAdForm
from sites.achetersanscom.ads.filtersets import HomeForSaleAdFilterSet


urlpatterns = patterns('',
    url(r'^(?P<slug>[-\w]+)$', AdDetailView.as_view(model=HomeForSaleAd), 
                                                            name="view"),
    url(r'^search/$', AdSearchView.as_view(model=HomeForSaleAd, 
                                         filterset_class=HomeForSaleAdFilterSet), 
                                                                  name='search'), 
    url(r'^search/(?P<search_id>\d+)/$', AdSearchView.as_view(model=HomeForSaleAd, 
                                         filterset_class=HomeForSaleAdFilterSet), 
                                                                  name='search'),
    url(r'^delete_search/(?P<pk>\d+)$', AdSearchDeleteView.as_view(), 
                                         name='delete_search'),
    url(r'^add/$', AdCreateView.as_view(model=HomeForSaleAd, 
                                        form_class=HomeForSaleAdForm), 
                                                             name='add'),
    url(r'^add/complete/$', CompleteView.as_view(), name='complete'),
    url(r'^(?P<pk>\d+)/edit$', AdUpdateView.as_view(model=HomeForSaleAd, 
                                        form_class=HomeForSaleAdForm), 
                                                            name='edit'),
    url(r'^(?P<pk>\d+)/delete$', AdDeleteView.as_view(model=HomeForSaleAd), 
                                                          name='delete'),
)