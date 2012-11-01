#-*- coding: utf-8 -*-
from django.dispatch import receiver

from geoads.signals import (geoad_new_interested_user,
    geoad_new_relevant_ad_for_search, geoad_user_message, geoad_vendor_message)

from homeads.mails import (BuyerToVendorMessageEmail,
    HomeAdCreatedMessageEmail, HomeAdUpdatedMessageEmail,
    NewPotentialBuyerToVendorMessageEmail, NewAdToBuyerMessageEmail, VendorToBuyerMessageEmail)


@receiver(geoad_new_interested_user)
def geoad_new_interested_user_callback(sender, ad, interested_user, **kwargs):
    email_context = {'to': ad.user.email, 'ad': ad}
    msg = NewPotentialBuyerToVendorMessageEmail(email_context, ad.user.email, ad=ad)
    msg.send()


@receiver(geoad_new_relevant_ad_for_search)
def geoad_new_relevant_ad_for_search_callback(sender, ad, relevant_search, **kwargs):
    email_context = {'to': relevant_search.ad_search.user.email, 'ad': ad}
    msg = NewAdToBuyerMessageEmail(email_context, relevant_search.ad_search.user.email, ad=ad)
    msg.send()


@receiver(geoad_user_message)
def geoad_user_message_callback(sender, ad, user, message, **kwargs):
    email_context = {'message': message, 'to': ad.user.email, 'from': user.email, 'ad': ad}
    msg = BuyerToVendorMessageEmail(email_context, ad.user.email, user.email, ad=ad)
    msg.send()


@receiver(geoad_vendor_message)
def geoad_vendor_message_callback(sender, ad, user, message, **kwargs):
    email_context = {'message': message, 'to': user.email, 'from': ad.user.email, 'ad': ad}
    msg = VendorToBuyerMessageEmail(email_context, ad.user.email, user.email, ad=ad)
    msg.send()


def home_ad_post_save_handler(sender, instance, created, **kwargs):
    email_context = {'to': instance.user.email, 'ad': instance}
    if created:
        msg = HomeAdCreatedMessageEmail(email_context, instance.user.email, ad=instance)
    else:
        msg = HomeAdUpdatedMessageEmail(email_context, instance.user.email, ad=instance)
    msg.send()
