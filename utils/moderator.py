# coding=utf-8
import oauth2 as oauth

from django.conf import settings
from django.template.defaultfilters import urlencode
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save

from moderation.moderator import GenericModerator
from moderation import moderation
from moderation.signals import post_moderation

from geoads.signals import ad_post_save_handler

from sites.louersanscom.ads.models import HomeForRentAd
from sites.louersanscom.ads.filtersets import HomeForRentAdFilterSet
from sites.achetersanscom.ads.models import HomeForSaleAd
from sites.achetersanscom.ads.filtersets import HomeForSaleAdFilterSet
from utils.managers import ModeratedAdManager


class AdModerator(GenericModerator):
    fields_exclude = ['update_date', 'create_date', 'delete_date']
    notify_moderator = True
    notify_user = True
    visibility_column = 'visible'
    moderation_manager_class = ModeratedAdManager  # allow geomanager + moderationmanager


moderation.register(HomeForRentAd, AdModerator)
moderation.register(HomeForSaleAd, AdModerator)


# need to remove signal ad and subclass ad_post_save_handler
post_save.disconnect(ad_post_save_handler, sender=HomeForRentAd, dispatch_uid="ad_post_save_handler_HomeForRentAd")
post_save.disconnect(ad_post_save_handler, sender=HomeForSaleAd, dispatch_uid="ad_post_save_handler_HomeForSaleAd")


def post_moderation_abstract_handler(sender, instance, status, **kwargs):
    # here I call signal function coming form django-geoads
    ad_post_save_handler(sender, instance, **kwargs)
    #
    content_type = ContentType.objects.get_for_model(instance)
    if content_type.model == 'homeforsalead':
        search_filter = HomeForSaleAdFilterSet
    if content_type.model == 'homeforrentad':
        search_filter = HomeForRentAdFilterSet
    if status == 1:
        # send on twitter
        token = oauth.Token(key=settings.TWITTER_ACCESS_TOKEN_KEY,
                            secret=settings.TWITTER_ACCESS_TOKEN_SECRET)
        consumer = oauth.Consumer(settings.TWITTER_CONSUMER_KEY,
                                  settings.TWITTER_CONSUMER_SECRET)
        client = oauth.Client(consumer, token)
        ad = HomeForSaleAd.objects.get(id=instance.moderated_object.changed_object.id)
        habitation_type = ad.get_habitation_type_display()
        price = ad.price
        surface = int(ad.surface)
        rooms = int(ad.nb_of_rooms)
        status = u'#achetersanscom %s - %s€ - %sm² - %s pièces' % (habitation_type,
                                                price, surface, rooms)
        pnt = GEOSGeometry('SRID=%s;%s' % (ad.location.srid, ad.location.wkt))
        latitude = pnt.y
        longitude = pnt.x
        params = 'status=%s&lat=%s&long=%s&display_coordinates=true' % (urlencode(status), latitude, longitude)
        #print params
        if not settings.DEBUG and settings.TWITTER_NOTIFICATION:
            resp, content = client.request(
                'http://api.twitter.com/1/statuses/update.xml?%s' % (params),
                "POST"
            )

post_moderation.connect(post_moderation_abstract_handler, dispatch_uid="post_moderation_abstract_handler")
