from django.conf.urls.defaults import *
from views import *

urlpatterns = patterns('',
    #url(r'^search/$', search, name='search'),
    url(r'^search/(?P<search_id>\d+)$', search, name='search'),
    url(r'^delete_search/(?P<search_id>\d+)$', delete_search, name='delete_search'),
    url(r'^add/$', add, name='add'),
    url(r'^(?P<ad_id>\d+)$', view, name='view'),
    url(r'^(?P<ad_id>\d+)/edit$', edit, name='edit'),
    url(r'^(?P<ad_id>\d+)/delete$', delete, name='delete'), 
)