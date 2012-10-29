#-*- coding: utf-8 -*-
from django.contrib.sites.models import Site
from utils.mails import AdEmailMultiAlternatives


class HomeEmail(AdEmailMultiAlternatives):
    """
    Class used to send multi alternavies email (text + html)
    for AcheterSansCom and LouerSansCom
    """
    def get_default_context(self):
        domain = Site.objects.get_current().domain
        if domain == 'achetersanscom.com':
            self.default_context = {'linkColor': '#20B2AB',
            'secondColor': '#FFB82E'}
        if domain == 'louersanscom.com':
            self.default_context = {'linkColor': '#9D81A1',
            'secondColor': 'Pink'}
        return self.default_context

    def get_default_images(self):
        domain = Site.objects.get_current().domain
        if domain == 'achetersanscom.com':
            self.default_files = (('img/home.png', 'logo'),
                ('img/shadow_bottom.jpg', 'shadow'))
        if domain == 'louersanscom.com':
            self.default_files = (('img/apartment.png', 'logo'),
                ('img/shadow_bottom.jpg', 'shadow'))
        return self.default_files


class UserSignIn(HomeEmail):
    """
    User Sign In
    """
    subject = u"[{{ site.name }}] Validation de votre inscription"
    template_name = 'emails/user_sign_in/body'


class BuyerToVendorMessageEmail(HomeEmail):
    """
    User message email from buyer to vendor for an Ad
    """
    subject = u'[{{ site.name }}] Nouveau message à propos de votre bien'
    template_name = 'emails/to_vendor_message/body'


class VendorToBuyerMessageEmail(HomeEmail):
    """
    User message email from vendor to buyer for an Ad
    """
    subject = u'[{{ site.name }}] Nouveau message à propos de votre recherche'
    template_name = 'emails/to_buyer_message/body'


class NewPotentialBuyerToVendorMessageEmail(HomeEmail):
    """
    Mail sent to vendor when a user has it search coincides with it ad
    """
    subject = u'[{{ site.name }}] Une nouvelle personne pourrait être interessée par votre bien'
    template_name = 'emails/to_vendor_potential_buyer/body'


class NewAdToBuyerMessageEmail(HomeEmail):
    """
    Mail sent to inform a user that a new ad corresponds to it search
    """
    subject = u'[{{ site.name }}] Un nouveau bien correspond à votre recherche'
    template_name = 'emails/to_buyer_potential_ad/body'