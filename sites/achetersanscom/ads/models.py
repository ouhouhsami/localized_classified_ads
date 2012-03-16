# coding=utf-8
from django.db import models
from django.utils.translation import ugettext as _
from autoslug import AutoSlugField

from ads.models import Ad


#
# HOME FOR SALE AD MODEL
#

HABITATION_TYPE_CHOICES = (
    ('0', _(u'Appartement')),
    ('1', _(u'Maison')),
    ('7', _(u'Parking')),
    ('8', _(u'Autres')),
)

ENERGY_CONSUMPTION_CHOICES = (
    ('A', _(u'A - ≤ 50')),
    ('B', _(u'B - 51 à 90')),
    ('C', _(u'C - 91 à 150')),
    ('D', _(u'D - 151 à 230')),
    ('E', _(u'E - 231 à 330')),
    ('F', _(u'F - 331 à 450')),
    ('G', _(u'G - > 450')),
)

EMISSION_OF_GREENHOUSE_GASES_CHOICES = (
    ('A', _(u'A - ≤ 5')),
    ('B', _(u'B - 6 à 10')),
    ('C', _(u'C - 11 à 20')),
    ('D', _(u'D - 21 à 35')),
    ('E', _(u'E - 36 à 55')),
    ('F', _(u'F - 56 à 80')),
    ('G', _(u'G - > 80')),
)

HEATING_CHOICES = (
    ('1', _(u'individuel gaz')),
    ('2', _(u'individuel électrique')),
    ('3', _(u'collectif gaz')),
    ('4', _(u'collectif fuel')),
    ('5', _(u'collectif réseau de chaleur')),
    ('13', _(u'autres'))
)


KITCHEN_CHOICES = (
    ('1', _(u'américaine')),
    ('2', _(u'séparée')),
    ('3', _(u'industrielle')),
    ('4', _(u'coin-cuisine')),
    ('5', _(u'belle vue')),
    ('6', _(u'sans vis à vis')),
    ('7', _(u'américaine équipée')),
    ('8', _(u'séparée équipée')),
    ('9', _(u'coin cuisine équipé')),
)


PARKING_CHOICES = (
    ('1', _(u'Place de parking')),
    ('2', _(u'Box fermé')),
)

FIREPLACE_CHOICES = (
    ('1', _(u'Foyer ouvert')),
    ('2', _(u'Insert')),
)

class HomeForSaleAd(Ad):
    """
    HomeFormSaleAd model

    """
    price = models.PositiveIntegerField(_(u"Prix (€)"))
    habitation_type	= models.CharField(_(u"Type de bien"), max_length=1, 
                                       choices=HABITATION_TYPE_CHOICES)
    surface = models.IntegerField(_(u"Surface habitable (m²)"))
    surface_carrez = models.IntegerField(_(u"Surface Loi Carrez (m²)"), 
                                         null=True, blank=True)
    nb_of_rooms	= models.PositiveIntegerField(_(u"Nombre de pièces"))
    nb_of_bedrooms = models.PositiveIntegerField(_(u"Nombre de chambres"))
    energy_consumption = models.CharField(_(u"Consommation énergétique (kWhEP/m².an)"), 
                                          max_length=1, 
                                          choices = ENERGY_CONSUMPTION_CHOICES, 
                                          null = True, blank = True)
    ad_valorem_tax = models.IntegerField(_(u'Taxe foncière (€)'), null = True,
                                         blank = True, 
                                         help_text=_(u"Montant annuel, sans espace, sans virgule"))
    housing_tax = models.IntegerField(_(u"Taxe d'habitation (€)"), null = True, 
                                      blank = True, help_text=_(u"Montant annuel, sans espace, sans virgule"))
    maintenance_charges = models.IntegerField(_(u'Charges (€)'), null = True, 
                                              blank = True, help_text=_(u"Montant mensuel, sans espace, sans virgule"))
    emission_of_greenhouse_gases = models.CharField(_(u"Émissions de gaz à effet de serre (kgeqCO2/m².an)"), 
                                                    max_length = 1, 
                                                    choices = EMISSION_OF_GREENHOUSE_GASES_CHOICES, 
                                                    null = True, blank = True)
    ground_surface = models.IntegerField(_(u'M²'), 
                                       null = True, blank = True)
    floor = models.PositiveIntegerField(_(u'Etage'), null = True, blank = True)
    ground_floor = models.BooleanField(_(u'Rez de chaussé'))
    top_floor = models.BooleanField(_(u'Dernier étage'))
    not_overlooked = models.BooleanField(_(u'Sans vis-à-vis'))
    elevator = models.BooleanField(_(u"Ascenceur"))
    intercom = models.BooleanField(_(u"Interphone"))
    digicode = models.BooleanField(_(u"Digicode"))
    doorman = models.BooleanField(_(u"Gardien"))
    heating = models.CharField(_(u"Chauffage"), max_length = 2, 
                               choices = HEATING_CHOICES, null = True, blank = True)
    kitchen = models.BooleanField(_(u"Cuisine équipée"))
    duplex = models.BooleanField(_(u"Duplex"))
    swimming_pool = models.BooleanField(_(u"Piscine"))
    alarm = models.BooleanField(_(u"Alarme"))
    air_conditioning = models.BooleanField(_(u"Climatisation"))
    fireplace = models.CharField(_(u"Cheminée"), max_length = 2,
                               choices = FIREPLACE_CHOICES, null = True, blank = True)
    terrace = models.IntegerField(_(u"Terrasse"), null = True, blank = True)
    balcony = models.IntegerField(_(u"Balcon"), null = True, blank = True)
    separate_dining_room = models.BooleanField(_(u"Cuisine séparée"))
    separate_toilet = models.IntegerField(_(u"Toilettes séparés"), null = True, blank = True)
    bathroom = models.IntegerField(_(u"Salle de bain"), null = True, blank = True)
    shower = models.IntegerField(_(u"Salle d'eau (douche)"), null = True, blank = True)
    separate_entrance = models.BooleanField(_(u"Entrée séparée"))
    cellar = models.BooleanField(_(u"Cave"))
    parking = models.CharField(_(u"Parking"), max_length = 2,
                               choices = PARKING_CHOICES, null = True, blank = True)
    orientation = models.CharField(_(u"Orientation"), max_length = 255, null = True, blank = True)

    def _icon(self):
        return "/static/img/home.png"
    icon = property(_icon)

    def get_full_description(instance):
        return "vente-%s-%spieces-%seuros-%sm2" % (instance.get_habitation_type_display(), 
                                               instance.nb_of_rooms, 
                                               instance.price, instance.surface)
    @models.permalink
    def get_absolute_url(self):
        return ('view', [str(self.slug)])  
    def __unicode__(self):
        return u'%s € - %s m² - %s pieces' % (self.price, self.surface, self.nb_of_rooms)
    class Meta:
        app_label = 'ads'


def format_search_resume(q):
    habitation_types_values = q.getlist('habitation_type')
    search_zone = _(u'non géolocalisée')
    if len(q['location']) > 0:
        search_zone = _(u'géolocalisée')
    habitation_types = ' '
    for i in habitation_types_values:
        habitation_types += HABITATION_TYPE_CHOICES[int(i)][1]
        if int(i) == len(habitation_types_values)-1:
            habitation_types += ' '
        else:
            habitation_types += ', '
    if len(habitation_types_values) == 0:
        habitation_types += _(u'sans type d\'habitation précisé')
    habitation_types += ''
    min_price = q.get('price_0', '')
    max_price = q.get('price_1', '')
    price = ''
    if len(min_price) > 0 and len(max_price) > 0:
        price = _(u'- entre %s et %s €') % (min_price, max_price)
    elif len(min_price) == 0 and len(max_price) > 0:
        price = _(u'- inférieur à %s €') % (max_price)
    elif len(min_price) > 0 and len(max_price) == 0:
        price = _(u'- supérieur à %s €') % (min_price)
    if len(min_price) == 0 and len(max_price) == 0:
        price = _(u'- sans critère de prix')

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

    return _('Recherche <i>%s</i> : <b>%s</b> %s %s %s') % (search_zone, 
                             habitation_types, price, surface, rooms)




