#-*- coding: utf-8 -*-

from django.db import models
from django.http import QueryDict
from django.utils.translation import ugettext as _
from django.dispatch import receiver
from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.template.loader import render_to_string

from autoslug import AutoSlugField

from geoads.models import Ad, AdSearch, AdSearchResult

from utils.models import ModeratedAd


# SPECIFIC AD MODELS 


#
# HOME FOR RENT AD MODEL
#

HABITATION_TYPE_CHOICES = (
    ('0', _(u'Appartement')),
    ('1', _(u'Maison')),
)


HEATING_CHOICES = (
    ('1', _(u'individuel gaz')),
    ('2', _(u'individuel électrique')),
    ('3', _(u'collectif gaz')),
    ('4', _(u'collectif fuel')),
    ('5', _(u'collectif réseau de chaleur')),
    ('13', _(u'autres'))
)



PARKING_CHOICES = (
    ('1', _(u'Place de parking')),
    ('2', _(u'Box fermé')),
)


class HomeForRentAd(ModeratedAd):
    """
    HomeFormRentAd model

    """
    price = models.PositiveIntegerField(_(u"Loyer"))
    colocation = models.BooleanField(_(u"Colocation possible"))
    furnished = models.TextField(_(u"Habitation meublée"),
        null=True, blank=True)
    habitation_type = models.CharField(_(u"Type de bien"), max_length=1,
        choices=HABITATION_TYPE_CHOICES)
    surface = models.IntegerField(_(u"Surface habitable"))
    surface_carrez = models.IntegerField(_(u"Surface Loi Carrez"),
        null=True, blank=True)
    nb_of_rooms = models.PositiveIntegerField(_(u"Nombre de pièces"))
    nb_of_bedrooms = models.PositiveIntegerField(_(u"Nombre de chambres"))
    housing_tax = models.IntegerField(_(u"Taxe d'habitation"), null=True,
        blank=True)
    maintenance_charges = models.IntegerField(_(u'Charges'), null=True,
        blank=True)
    ground_surface = models.IntegerField(_(u'M²'),
        null=True, blank=True)
    floor = models.PositiveIntegerField(_(u'Etage'), null=True, blank=True)
    ground_floor = models.BooleanField(_(u'Rez de chaussé'))
    top_floor = models.BooleanField(_(u'Dernier étage'))
    not_overlooked = models.BooleanField(_(u'Sans vis-à-vis'))
    elevator = models.BooleanField(_(u"Ascenceur"))
    intercom = models.BooleanField(_(u"Interphone"))
    digicode = models.BooleanField(_(u"Digicode"))
    doorman = models.BooleanField(_(u"Gardien"))
    heating = models.CharField(_(u"Chauffage"), max_length=2,
        choices=HEATING_CHOICES, null=True, blank=True)
    duplex = models.BooleanField(_(u"Duplex"))
    terrace = models.IntegerField(_(u"Terrasse"), null=True, blank=True)
    balcony = models.IntegerField(_(u"Balcon"), null=True, blank=True)
    separate_dining_room = models.BooleanField(_(u"Cuisine séparée"))
    separate_toilet = models.IntegerField(_(u"Toilettes séparés"), null=True, blank=True)
    bathroom = models.IntegerField(_(u"Salle de bain"), null=True, blank=True)
    shower = models.IntegerField(_(u"Salle d'eau (douche)"), null=True, blank=True)
    parking = models.CharField(_(u"Parking"), max_length=2,
        choices=PARKING_CHOICES, null=True, blank=True)
    orientation = models.CharField(_(u"Orientation"), max_length=255,
        null=True, blank=True)

    def _icon(self):
        return "/static/img/apartment.png"
    icon = property(_icon)

    def get_full_description(self, instance=None):
        return _(u"location-%s-%spieces-%se_par_mois-%sm2") % (self.get_habitation_type_display(), 
                                               self.nb_of_rooms, 
                                               self.price, self.surface)
    def __unicode__(self):
        return _(u'%s e par mois - %s m2 - %s pieces') % (self.price, self.surface, self.nb_of_rooms)

    @models.permalink
    def get_absolute_url(self):
        return ('view', [str(self.slug)])

    class Meta:
        app_label = 'ads'


class HomeForRentAdSearch(AdSearch):
    """this class acts as proxy for AdSearch model"""
    def __unicode__(self):
        q = QueryDict(self.search)
        return format_search_resume(q)

    class Meta:
        proxy = True


class HomeForRentAdSearchResult(AdSearchResult):
    """
    this class acts as proxy for AdPotentialBuyersView model
    this is a way to get the above __unicode__ for related HomeForSaleAdSearch instance
    """
    @property
    def ad_search(self):
        # joel cross proposition
        # http://stackoverflow.com/questions/3891880/django-proxy-model-and-foreignkey
        return HomeForRentAdSearch.objects.get(id=self.ad_search_id)
        # below approach should be better, without hitting db may be, but doesn't work
        #new_inst = HomeForSaleAdSearch()
        #new_inst.__dict__ = super(HomeForSaleAdSearch, self).ad_search.__dict__
        #return new_inst

    class Meta:
        proxy = True


def format_search_resume(q):
    habitation_types_values = q.getlist('habitation_type')
    search_zone = _(u'non géolocalisée')
    if len(q['location']) > 0:
        search_zone = _(u'géolocalisée')
    habitation_types = ' '
    for i in habitation_types_values:
        if isinstance(i, int):
            habitation_types += HABITATION_TYPE_CHOICES[int(i)][1]
            if int(i) == len(habitation_types_values)-1:
                habitation_types += ' '
            else:
                habitation_types += ', '
        else:
            habitation_types += _(u'sans type d\'habitation précisé')
    #if len(habitation_types_values) == 0:
    #    habitation_types += u'sans type d\'habitation précisé'
    habitation_types += ''
    min_price = q.get('price_0', '')
    max_price = q.get('price_1', '')
    price = ''
    if len(min_price) > 0 and len(max_price) > 0:
        price = u'- entre %s et %s €/mois' % (min_price, max_price)
    elif len(min_price) == 0 and len(max_price) > 0:
        price = u'- inférieur à %s €/mois' % (max_price)
    elif len(min_price) > 0 and len(max_price) == 0:
        price = u'- supérieur à %s €/mois' % (min_price)
    if len(min_price) == 0 and len(max_price) == 0:
        price = u'- sans critère de prix'

    min_surface = q.get('surface_0', '')
    max_surface = q.get('surface_1', '')
    surface = ''
    if len(min_surface) > 0 and len(max_surface) > 0:
        surface = _(u'- entre %s et %s m²') % (min_surface, max_surface)
    elif len(min_surface) == 0 and len(max_surface) > 0:
        surface = _(u'- inférieur à %s m²') % (max_surface)
    elif len(min_surface) > 0 and len(max_surface) == 0:
        surface = _(u'- supérieur à %s m²') % (min_surface)
    if len(min_surface) == 0 and len(max_surface) == 0:
        surface = _(u'- sans critère de surface')

    min_rooms = str(q.get('nb_of_rooms_0', ''))
    max_rooms = str(q.get('nb_of_rooms_1', ''))
    rooms = ''
    if len(min_rooms) > 0 and len(max_rooms) > 0:
        rooms = _(u'- entre %s et %s pièces') % (min_rooms, max_rooms)
    elif len(min_rooms) == 0 and len(max_rooms) > 0:
        rooms = _(u'- inférieur à %s pièces') % (max_rooms)
    elif len(min_rooms) > 0 and len(max_rooms) == 0:
        rooms = _(u'- supérieur à %s pièces') % (min_rooms)

    return _(u'Recherche <i>%s</i> : <b>%s</b> %s %s %s') % (search_zone,
                             habitation_types, price, surface, rooms)


# TODO below is duplicated with the same in HomeForSale !
@receiver(post_save, sender=HomeForRentAd)
def home_for_rent_ad_post_save_handler(sender, instance, created, **kwargs):
    if created:
        message = render_to_string('emails/ad_create_email_message.txt')
        subject = render_to_string('emails/ad_create_email_subject.txt',
                          {'site_name': Site.objects.get_current().name})
        send_mail(subject, message, 'contact@achetersanscom.com',
              [instance.user.email], fail_silently=True)
    else:
        message = render_to_string(
                  'emails/ad_update_email_message.txt', {})
        subject = render_to_string(
                  'emails/ad_update_email_subject.txt',
                         {'site_name': Site.objects.get_current().name})
        send_mail(subject, message, 'contact@achetersanscom.com',
                  [instance.user.email],
                          fail_silently=True)

# VERY IMPORTANT TO PLACE THIS IMPORT AT THE BOTTOM
# so that abstract class and subclass signal dispatcher
# is available for this model
# and also the signal disconnect, and connect for moderation
from geoads.receivers import *
from homeads.moderator import *
