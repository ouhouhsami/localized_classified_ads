"""
AcheterSansCom urls.py

"""
from django.conf.urls.defaults import patterns, url
from geoads.views import (AdSearchView, AdDetailView,
                              AdSearchDeleteView, AdCreateView,  AdUpdateView,
                              CompleteView, AdDeleteView)
from sites.achetersanscom.ads.models import HomeForSaleAd, HomeForSaleAdSearch
from sites.achetersanscom.ads.forms import HomeForSaleAdForm
from sites.achetersanscom.ads.filtersets import HomeForSaleAdFilterSet
from sites.achetersanscom.ads.views import HomeForSaleAdSearchView
from sites.achetersanscom.ads.forms import PrettyAdPictureForm


urlpatterns = patterns('',
    url(r'^(?P<slug>[-\w]+)$', AdDetailView.as_view(model=HomeForSaleAd),
                                                            name="view"),
    url(r'^search/$', HomeForSaleAdSearchView.as_view(), name='search'),
    url(r'^search/(?P<search_id>\d+)/$', HomeForSaleAdSearchView.as_view(), name='search'),
    url(r'^delete_search/(?P<pk>\d+)$', AdSearchDeleteView.as_view(model=HomeForSaleAdSearch),
                                         name='delete_search'),
    url(r'^add/$', AdCreateView.as_view(model=HomeForSaleAd,
                                        form_class=HomeForSaleAdForm, ad_picture_form=PrettyAdPictureForm),
                                                             name='add'),
    url(r'^add/complete/$', CompleteView.as_view(), name='complete'),
    url(r'^(?P<pk>\d+)/edit$', AdUpdateView.as_view(model=HomeForSaleAd,
                                        form_class=HomeForSaleAdForm, ad_picture_form=PrettyAdPictureForm),
                                                            name='edit'),
    url(r'^(?P<pk>\d+)/delete$', AdDeleteView.as_view(model=HomeForSaleAd),
                                                          name='delete'),
)
