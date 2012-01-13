# coding=utf-8

from django.db import models
from autoslug import AutoSlugField

from ads.models import Ad

# SPECIFIC AD MODELS 


#
# HOME FOR RENT AD MODEL
#

HABITATION_TYPE_CHOICES = (
    ('0', 'Appartement'),
    ('1', 'Maison'),
)


HEATING_CHOICES = (
    ('1', 'individuel gaz'),
    ('2', 'individuel électrique'),
    ('3', 'collectif gaz'),
    ('4', 'collectif fuel '),
    ('5', 'collectif réseau de chaleur'),
    ('13', 'autres')
)



PARKING_CHOICES = (
    #('0', 'Non'),
    ('1', 'Place de parking'),
    ('2', 'Box fermé'),
)


class HomeForRentAd(Ad):
    """HomeFormRentAd model

    """
    price = models.PositiveIntegerField("Loyer (€/mois)")
    slug = AutoSlugField(populate_from='get_full_description', always_update=True, unique=True)
    colocation = models.BooleanField("Colocation possible")
    furnished = models.TextField("Habitation meublée", null=True, blank=True)
    habitation_type	= models.CharField("Type de bien", max_length = 1, 
                                       choices = HABITATION_TYPE_CHOICES)
    surface = models.IntegerField("Surface habitable (m²)")
    surface_carrez = models.IntegerField("Surface Loi Carrez (m²)", 
                                         null = True, blank = True)
    nb_of_rooms	= models.PositiveIntegerField("Nombre de pièces")
    nb_of_bedrooms = models.PositiveIntegerField("Nombre de chambres")
    housing_tax = models.IntegerField('Taxe d\'habitation (€/an)', null = True, 
                                      blank = True)
    maintenance_charges = models.IntegerField('Charges (€/mois)', null = True, 
                                              blank = True)
    ground_surface = models.IntegerField('M²', 
                                       null = True, blank = True)
    floor = models.PositiveIntegerField('Etage', null = True, blank = True)
    ground_floor = models.BooleanField('Rez de chaussé')
    top_floor = models.BooleanField('Dernier étage')
    not_overlooked = models.BooleanField('Sans vis-à-vis')
    elevator = models.BooleanField("Ascenceur")
    intercom = models.BooleanField("Interphone")
    digicode = models.BooleanField("Digicode")
    doorman = models.BooleanField("Gardien")
    heating = models.CharField("Chauffage", max_length = 2, 
                               choices = HEATING_CHOICES, null = True, blank = True)
    duplex = models.BooleanField("Duplex")
    terrace = models.IntegerField("Terrasse", null = True, blank = True)
    balcony = models.IntegerField("Balcon", null = True, blank = True)
    separate_dining_room = models.BooleanField("Cuisine séparée")
    separate_toilet = models.IntegerField("Toilettes séparés", null = True, blank = True)
    bathroom = models.IntegerField("Salle de bain", null = True, blank = True)
    shower = models.IntegerField("Salle d'eau (douche)", null = True, blank = True)
    parking = models.CharField("Parking", max_length = 2,
                               choices = PARKING_CHOICES, null = True, blank = True)
    orientation = models.CharField("Orientation", max_length = 255, null = True, blank = True)

    def _icon(self):
        return "/static/img/apartment.png"
    icon = property(_icon)

    def get_full_description(instance):
        return "location-%s-%spieces-%se_par_mois-%sm2" % (instance.get_habitation_type_display(), 
                                               instance.nb_of_rooms, 
                                               instance.price, instance.surface)
    def __unicode__(self):
        return '%s e par mois - %s m2 - %s pieces' % (self.price, self.surface, self.nb_of_rooms)

    @models.permalink
    def get_absolute_url(self):
        return ('view', [str(self.slug)])

    class Meta:
        app_label = 'ads'

def format_search_resume(q):
    habitation_types_values = q.getlist('habitation_type')
    search_zone = u'non géolocalisée'
    if len(q['location']) > 0:
        search_zone = u'géolocalisée'
    habitation_types = ' '
    for i in habitation_types_values:
        if isinstance(i, int):
            habitation_types += HABITATION_TYPE_CHOICES[int(i)][1]
            if int(i) == len(habitation_types_values)-1:
                habitation_types += ' '
            else:
                habitation_types += ', '
        else:
            habitation_types += u'sans type d\'habitation précisé'
    #if len(habitation_types_values) == 0:
    #    habitation_types += u'sans type d\'habitation précisé'
    habitation_types += ''
    min_price = q.get('price_0', '')
    max_price = q.get('price_1', '')
    price = ''
    if len(min_price) > 0 and len(max_price) > 0:
        price = u'- entre %s et %s/mois' % (min_price, max_price)
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
        surface = u'- entre %s et %s m²' % (min_surface, max_surface)
    elif len(min_surface) == 0 and len(max_surface) > 0:
        surface = u'- inférieur à %s m²' % (max_surface)
    elif len(min_surface) > 0 and len(max_surface) == 0:
        surface = u'- supérieur à %s m²' % (min_surface)
    if len(min_surface) == 0 and len(max_surface) == 0:
        surface = u'- sans critère de surface'

    min_rooms = str(q.get('nb_of_rooms_0', ''))
    max_rooms = str(q.get('nb_of_rooms_1', ''))
    rooms = ''
    if len(min_rooms) > 0 and len(max_rooms) > 0:
        rooms = u'- entre %s et %s pièces' % (min_rooms, max_rooms)
    elif len(min_rooms) == 0 and len(max_rooms) > 0:
        rooms = u'- inférieur à %s pièces' % (max_rooms)
    elif len(min_rooms) > 0 and len(max_rooms) == 0:
        rooms = u'- supérieur à %s pièces' % (min_rooms)

    return 'Recherche <i>%s</i> : <b>%s</b> %s %s %s' % (search_zone, 
                             habitation_types, price, surface, rooms)