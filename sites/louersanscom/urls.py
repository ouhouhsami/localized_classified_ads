"""
louersanscom urls.py

"""
from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import redirect_to

from profiles.views import UserProfileDetailView
from sites.louersanscom.ads.models import HomeForRentAd, HomeForRentAdSearch

urlpatterns = patterns('',
    ('^$', redirect_to, {'url': '/annonce/search/'}),
    url(r'^annonce/', include('sites.louersanscom.ads.urls')),
    url(r'^accounts/(?P<slug>(?!signout|signup|signin)[\.\w]+)/$', 
            UserProfileDetailView.as_view(ad_model=HomeForRentAd, 
                                          ad_search_model=HomeForRentAdSearch), 
                                     name='userena_profile_detail'),
    url(r'^', include('localized_classified_ads.urls')),
)
