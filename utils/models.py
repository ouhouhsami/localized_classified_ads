#-*- coding: utf-8 -*-
from django.db import models
from django.dispatch import receiver
from django.contrib.sites.models import Site

from geoads.models import Ad
from geoads.signals import (geoad_new_interested_user,
    geoad_new_relevant_ad_for_search, geoad_user_message, geoad_vendor_message)

from homeads.mails import (BuyerToVendorMessageEmail,
    NewPotentialBuyerToVendorMessageEmail, NewAdToBuyerMessageEmail, VendorToBuyerMessageEmail)


class ModeratedAd(Ad):
    visible = models.BooleanField()

    class Meta:
        abstract = True
