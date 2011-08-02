# coding=utf-8
from django.db import models
from django.contrib.gis.db import models
import floppyforms
from profiles.models import UserProfile
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from moderation.fields import SerializedObjectField
from django.http import QueryDict
from moderation.managers import ModerationObjectsManager

# GENERIC AD MODELS

class AdPicture(models.Model):

    def upload_path(self, filename):
        # line below to fix : app_label is not model_name, but always ad which is bad
        # we should have /ad/homeforsalead/id/image.jpg
        #return 'pictures/%s/%s/%s' % (self.content_type.app_label, self.content_object.id, filename)
        return 'pictures/%s' % (filename)

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    title = models.CharField(max_length = 255)
    #image = models.ImageField(upload_to = upload_path)
    image = models.ImageField(upload_to='pictures/')
    #order = models.PositiveIntegerField() 

class AdContact(models.Model):
    user_profile = models.ForeignKey(UserProfile)
    content_type = models.ForeignKey(ContentType)
    object_pk = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey(ct_field="content_type",
                                               fk_field="object_pk")
    message = models.TextField()

class AdSearch(models.Model):
    search = models.CharField(max_length=2550)
    user_profile = models.ForeignKey(UserProfile)   
    create_date = models.DateTimeField(auto_now_add = True)  
    content_type = models.ForeignKey(ContentType)

class Ad(models.Model):
    """Ad abstract base model

    """
    title = models.CharField("Titre", max_length = 255, 
                                       help_text="Titre de votre annonce")
    user_profile = models.ForeignKey(UserProfile)
    description = models.TextField("", 
                                       null = True, blank = True)
    location = models.PointField(srid=900913)
    pictures = generic.GenericRelation(AdPicture)
    update_date = models.DateTimeField(auto_now = True)
    create_date = models.DateTimeField(auto_now_add = True) 
    delete_date = models.DateTimeField(null = True, blank = True)

    objects = models.GeoManager()

    class Meta:
        abstract = True
    
    def __unicode__(self):
        return self.title


# SPECIFIC AD MODELS 


#
# HOME FOR SALE AD MODEL
#

HABITATION_TYPE_CHOICES = (
    ('0', 'appartement'),
    ('1', 'maison'),
    #('2', 'loft/atelier/surface'),
    #('3', 'bureau'),
    #('4', 'boutique'),
    #('5', 'local commercial'),
    #('6', 'immeuble'),
    ('7', 'parking'),
    ('8', 'autres'),
)

ENERGY_CONSUMPTION_CHOICES = (
    ('A', 'A - ≤50'),
    ('B', 'B - 51 à 90'),
    ('C', 'C - 91 à 150'),
    ('D', 'D - 151 à 230'),
    ('E', 'E - 231 à 330'),
    ('F', 'F - 331 à 450'),
    ('G', 'G - >450'),
)

EMISSION_OF_GREENHOUSE_GASES_CHOICES = (
    ('A', 'A - ≤5'),
    ('B', 'B - 6 à 10'),
    ('C', 'C - 11 à 20'),
    ('D', 'D - 21 à 35'),
    ('E', 'E - 36 à 55'),
    ('F', 'F - 56 à 80'),
    ('G', 'G - >80'),
)

HEATING_CHOICES = (
    ('1', 'gaz'),
    ('2', 'collectif'),
    ('3', 'individuel gaz'),
    ('4', 'collectif gaz'),
    ('5', 'fuel'),
    ('6', 'electrique'),
    ('7', 'collectif fuel'),
    ('8', 'individuel'),
    ('9', 'individuel electrique'),
    ('10', 'sol'),
    ('11', 'gaz sol'),
    ('12', 'collectif radiateur'),
    ('13', 'autres')
)

KITCHEN_CHOICES = (
    ('1', 'américaine'),
    ('2', 'séparée'),
    ('3', 'industrielle'),
    ('4', 'coin-cuisine'),
    ('5', 'belle vue'),
    ('6', 'sans vis à vis'),
    ('7', 'américaine équipée'),
    ('8', 'séparée équipée'),
    ('9', 'coin cuisine équipé'),
)


PARKING_CHOICES = (
    ('0', 'Non'),
    ('1', 'Ouvert'),
    ('2', 'Fermé'),
)

ORIENTATION_CHOICES = (
    ('1', 'sud'),
    ('2', 'est'),
    ('3', 'nord'),
    ('4', 'ouest'),
    #('5', 'belle vue'),
    #('6', 'sans vis à vis'),
)

class HomeAd(Ad):
    habitation_type	= models.CharField("Type de bien", max_length = 1, 
                                       choices = HABITATION_TYPE_CHOICES)
    surface = models.FloatField("Surface (m², hors terrain)")
    nb_of_rooms	= models.PositiveIntegerField("Nombre de pièces")
    nb_of_bedrooms = models.PositiveIntegerField("Nombre de chambres")
    energy_consumption = models.CharField("Consommation énergétique (kWhEP/m².an)", 
                                          max_length = 1, 
                                          choices = ENERGY_CONSUMPTION_CHOICES)
    emission_of_greenhouse_gases = models.CharField("Émissions de gaz à effet de serre (kgeqCO2/m².an)", 
                                                    max_length = 1, 
                                                    choices = EMISSION_OF_GREENHOUSE_GASES_CHOICES)
    ground_surface = models.FloatField('Surface du terrain', 
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
    #kitchen = models.CharField("Cuisine", max_length = 2,
    #                           choices = KITCHEN_CHOICES, null = True, blank = True)
    kitchen = models.BooleanField("Cuisine équipée")
    duplex = models.BooleanField("Duplex")
    swimming_pool = models.BooleanField("Piscine")
    alarm = models.BooleanField("Alarme")
    air_conditioning = models.BooleanField("Climatisation")
    fireplace = models.BooleanField("Cheminée")
    #parquet = models.BooleanField("Parquet")
    terrace = models.BooleanField("Terrasse")
    balcony = models.BooleanField("Balcon")
    separate_dining_room = models.BooleanField("Cuisine séparée")
    #living_room = models.BooleanField("Séjour")
    separate_toilet = models.BooleanField("Toilettes séparés")
    bathroom = models.BooleanField("Salle de bain")
    shower = models.BooleanField("Salle d'eau (douche)")
    separate_entrance = models.BooleanField("Entrée séparée")
    cellar = models.BooleanField("Cave")
    #cupboards = models.BooleanField("Placards")
    parking = models.CharField("Parking", max_length = 2,
                               choices = PARKING_CHOICES, null = True, blank = True)
    #open_parking = models.BooleanField("Parking ouvert")
    #box = models.BooleanField("Parking fermé / garage")
    orientation = models.CharField("Orientation", max_length = 1, 
                                   choices = ORIENTATION_CHOICES, 
                                   null = True, blank = True)
    class Meta:
        abstract = True

class HomeForSaleAd(HomeAd):
    """HomeFormSaleAd model

    """
    price = models.PositiveIntegerField("Prix (€)")
    #objects = ModerationObjectsManager()
    #objects = models.GeoManager()
    @models.permalink
    def get_absolute_url(self):
        return ('view', [str(self.id)])  


class HomeForRentAd(HomeAd):
    """HomeFormRentAd model

    """
    price = models.PositiveIntegerField("Loyer", help_text="Loyer du bien en Euros par mois")
    colocation = models.BooleanField("Colocation possible")
    furnished = models.BooleanField("Appartement meublé")

    @models.permalink
    def get_absolute_url(self):
        return ('view', [str(self.id)])  
'''
class HomeForSaleSearch(models.Model):
    search = models.CharField(max_length=2550)
    user_profile = models.ForeignKey(UserProfile)   
    create_date = models.DateTimeField(auto_now_add = True)   
    def __unicode__(self):
        q = QueryDict(self.search)
        
        min_price = q.get('price_0', '')
        max_price = q.get('price_1', '')
        price = ''
        if len(min_price) > 0 and len(max_price) > 0:
            price = u'entre %s et %s €' % (min_price, max_price)
        elif len(min_price) == 0 and len(max_price) > 0:
            price = u'inférieur à %s €' % (max_price)
        elif len(min_price) > 0 and len(max_price) == 0:
            price = u'supérieur à %s €' % (min_price)
        
        min_surface = q.get('surface_0', '')
        max_surface = q.get('surface_1', '')
        surface = ''
        if len(min_surface) > 0 and len(max_surface) > 0:
            surface = u'entre %s et %s m2' % (min_surface, max_surface)
        elif len(min_surface) == 0 and len(max_surface) > 0:
            surface = u'inférieur à %s m2' % (max_surface)
        elif len(min_surface) > 0 and len(max_surface) == 0:
            surface = u'supérieur à %s m2' % (min_surface)
        
        min_rooms = str(q.get('nb_of_rooms_0', ''))
        max_rooms = str(q.get('nb_of_rooms_1', ''))
        rooms = ''
        if len(min_rooms) > 0 and len(max_rooms) > 0:
            rooms = u'entre %s et %s pièces' % (min_rooms, max_rooms)
        elif len(min_rooms) == 0 and len(max_rooms) > 0:
            rooms = u'inférieur à %s pièces' % (max_rooms)
        elif len(min_rooms) > 0 and len(max_rooms) == 0:
            rooms = u'supérieur à %s pièces' % (min_rooms)

        return '%s %s %s' % (price, surface, rooms)
    #pretty_view = property(_get_pretty_view)        
'''