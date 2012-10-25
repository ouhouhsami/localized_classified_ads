#-*- coding: utf-8 -*-

from django.db import models
from django.dispatch import receiver
from django.contrib.sites.models import Site

from geoads.models import Ad
from geoads.signals import (geoad_new_interested_user,
    geoad_new_relevant_ad_for_search, goead_user_message, geaod_vendor_message)

from utils.nicemails import send_nice_email


class ModeratedAd(Ad):
    visible = models.BooleanField()

    class Meta:
        abstract = True


def get_defaults():
    domain = Site.objects.get_current().domain
    if domain == 'achetersanscom.com':
        return {'images': (('img/home.png', 'logo'), ('img/shadow_bottom.jpg', 'shadow')),
            'base_ctx': {'linkColor': '#20B2AB', 'secondColor': '#FFB82E'}
        }
    else:
        return {'images': (('img/apartment.png', 'logo'), ('img/shadow_bottom.jpg', 'shadow')),
            'base_ctx': {'linkColor': '#9D81A1', 'secondColor': 'Pink'}
        }


@receiver(geoad_new_interested_user)
def geoad_new_interested_user_callback(sender, **kwargs):
    print("----------------------------------------> geoad_new_interested_user")


@receiver(geoad_new_relevant_ad_for_search)
def geoad_new_relevant_ad_for_search_callback(sender, **kwargs):
    print("----------------------------------------> geoad_new_relevant_ad_for_search")


@receiver(goead_user_message)
def goead_user_message_callback(sender, ad, user, message, **kwargs):
    #images = (('img/home.png', 'logo'), ('img/shadow_bottom.jpg', 'shadow'))
    email_context = {'site': Site.objects.get_current(), 'message': message,
        'to': ad.user.email, 'from': user.email, 'ad': ad,
        'linkColor': '#20B2AB', 'secondColor': '#FFB82E'}
    email_context.update(get_defaults()['base_ctx'])
    images = get_defaults()['images']
    send_nice_email('emails/to_vendor_message/body', email_context,
        u'[{{ site.name }}] Nouveau message à propos de votre bien', ad.user.email, user.email, images)


@receiver(geaod_vendor_message)
def geaod_vendor_message_callback(sender, **kwargs):
    print("----------------------------------------> geaod_vendor_message")
