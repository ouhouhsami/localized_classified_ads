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


class Ad(models.Model):
    """Ad abstract base model

    """
    title = models.CharField("Titre", max_length = 255, 
                                       help_text="Titre de votre annonce")
    user_profile = models.ForeignKey(UserProfile)
    description = models.TextField("Description", 
                                       null = True, blank = True, 
                                       help_text="Description de votre bien")
    location = models.PointField(srid=900913)
    update_date = models.DateTimeField(auto_now = True)
    create_date = models.DateTimeField(auto_now_add = True) 
    delete_date = models.DateTimeField(null = True, blank = True)

    objects = models.GeoManager()

    class Meta:
        abstract = True
    
    def __unicode__(self):
        return self.title

HABITATION_TYPE_CHOICES = (
    ('0', 'appartement'),
    ('1', 'maison / villa'),
    ('2', 'loft/atelier/surface'),
    ('3', 'bureau'),
    ('4', 'boutique'),
    ('5', 'local commercial'),
    ('6', 'immeuble'),
    ('7', 'parking'),
    ('8', 'divers'),
)

ENERGY_CONSUMPTION_CHOICES = (
    ('A', 'A'),
    ('B', 'B'),
    ('C', 'C'),
    ('D', 'D'),
    ('E', 'E'),
    ('F', 'F'),
    ('G', 'G'),
)

EMISSION_OF_GREENHOUSE_GASES_CHOICES = (
    ('A', 'A'),
    ('B', 'B'),
    ('C', 'C'),
    ('D', 'D'),
    ('E', 'E'),
    ('F', 'F'),
    ('G', 'G'),
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

ORIENTATION_CHOICES = (
    ('1', 'sud'),
    ('2', 'est'),
    ('3', 'nord'),
    ('4', 'ouest'),
    ('5', 'belle vue'),
    ('6', 'sans vis à vis'),
)

class HomeForSaleAd(Ad):

    price = models.IntegerField("Prix", help_text="Prix du bien en Euros")
    habitation_type	= models.CharField("Type d'habitation", max_length = 1, 
                                       choices = HABITATION_TYPE_CHOICES)
    surface = models.FloatField("Surface", 
                                help_text="Surface de votre bien en mètres carrés")
    nb_of_rooms	= models.IntegerField("Nombre de pièces")
    nb_of_bedrooms = models.IntegerField("Nombre de chambres")
    energy_consumption = models.CharField("Consommation énergétique", 
                                          max_length = 1, 
                                          choices = ENERGY_CONSUMPTION_CHOICES)
    emission_of_greenhouse_gases = models.CharField("Émissions de gaz à effet de serre", 
                                                    max_length = 1, 
                                                    choices = EMISSION_OF_GREENHOUSE_GASES_CHOICES)
    ground_surface = models.FloatField('Surface du terrain', 
                                       null = True, blank = True)
    floor = models.IntegerField('Etage', null = True, blank = True)
    top_floor = models.BooleanField('Dernier étage')
    elevator = models.BooleanField("Ascenceur")
    intercom = models.BooleanField("Interphone")
    digicode = models.BooleanField("Digicode")
    doorman = models.BooleanField("Gardien")
    heating = models.CharField("Chauffage", max_length = 2, 
                               choices = HEATING_CHOICES, null = True, blank = True)
    kitchen = models.CharField("Cuisine", max_length = 2,
                               choices = KITCHEN_CHOICES, null = True, blank = True)
    duplex = models.BooleanField("Duplex")
    swimming_pool = models.BooleanField("Piscine")
    alarm = models.BooleanField("Alarme")
    air_conditioning = models.BooleanField("Climatisation")
    fireplace = models.BooleanField("Cheminée")
    parquet = models.BooleanField("Parquet")
    terrace = models.BooleanField("Terrasse")
    balcony = models.BooleanField("Balcon")
    separate_dining_room = models.BooleanField("Salle à manger séparée")
    living_room = models.BooleanField("Séjour")
    separate_toilet = models.BooleanField("Toilettes séparés")
    bathroom = models.BooleanField("Salle de bain")
    shower = models.BooleanField("Salle d'eau (douche)")
    separate_entrance = models.BooleanField("Entrée séparée")
    cellar = models.BooleanField("Cave")
    cupboards = models.BooleanField("Placards")
    open_parking = models.BooleanField("Parking ouvert")
    box = models.BooleanField("Parking fermé / garage")
    orientation = models.CharField("Orientation", max_length = 1, 
                                   choices = ORIENTATION_CHOICES, 
                                   null = True, blank = True)

    #d_objects = ModerationObjectsManager()
    # objects = models.GeoManager()
    

class HomeForSaleAdPicture(models.Model): 

    def upload_path(self, filename):
        return 'pictures/%s/%s' % (self.homeforsalead.id, filename)

    homeforsalead	= models.ForeignKey(HomeForSaleAd)
    title 			= models.CharField(max_length = 255)
    image 			= models.ImageField(upload_to = upload_path)
    order 			= models.PositiveIntegerField()

    def __unicode__(self):
        return self.title

class AdContact(models.Model):
    user_profile = models.ForeignKey(UserProfile)
    content_type = models.ForeignKey(ContentType)
    object_pk = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey(ct_field="content_type",
                                               fk_field="object_pk")
    message = models.TextField()

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