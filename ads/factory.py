# -*- coding: utf-8 -*-
import decimal
import random
import mockups
from datetime import datetime
from models import HomeForSaleAd
from mockups import Mockup, Factory
from mockups import generators
from django.contrib.auth.models import User
from moderation.models import ModeratedObject


class GeoPointGenerator(generators.Generator):
    def __init__(self, *args, **kwargs):
        super(GeoPointGenerator, self).__init__(*args, **kwargs)

    def generate(self):
        coord_0 = decimal.Decimal(str(random.randrange(2003750834)/100 - 20037508.34/2))
        coord_1 = decimal.Decimal(str(random.randrange(2003750834)/100 - 20037508.34/2))
        value = 'POINT(%s %s)' % (coord_0, coord_1)
        return value

class HomeForSaleAdFactory(Factory):
    description = generators.LoremWordGenerator(20)
    location = GeoPointGenerator()
    surface = generators.IntegerGenerator(min_value=7, max_value=450)
    nb_of_rooms	= generators.IntegerGenerator(min_value=1, max_value=9)
    nb_of_bedrooms = generators.IntegerGenerator(min_value=1, max_value=9)
    price = generators.IntegerGenerator(min_value=8000, max_value=10000000)
    #habitation_type = generators.ChoiceGenerator(choices = HABITATION_TYPE_CHOICES)
    update_date = generators.DateTimeGenerator(max_date=datetime.now())
    create_date = generators.DateTimeGenerator(max_date=datetime.now()) 
    delete_date = generators.StaticGenerator(None)
    #energy_consumption = generators.ChoiceGenerator(choices = ENERGY_CONSUMPTION_CHOICES)
    #emission_of_greenhouse_gases = generators.ChoiceGenerator(choices = EMISSION_OF_GREENHOUSE_GASES_CHOICES)
    ground_surface = generators.IntegerGenerator(min_value=0, max_value=10000)
    floor = generators.IntegerGenerator(min_value=0, max_value=40)
    ground_floor = generators.BooleanGenerator()
    not_overlooked = generators.BooleanGenerator()
    top_floor = generators.BooleanGenerator()
    elevator = generators.BooleanGenerator()
    intercom = generators.BooleanGenerator()
    digicode = generators.BooleanGenerator()
    doorman = generators.BooleanGenerator()
    #heating = generators.ChoiceGenerator(choices = HEATING_CHOICES)
    #kitchen = generators.ChoiceGenerator(choices = KITCHEN_CHOICES)
    duplex = generators.BooleanGenerator()
    swimming_pool = generators.BooleanGenerator()
    alarm = generators.BooleanGenerator()
    air_conditioning = generators.BooleanGenerator()
    fireplace = generators.BooleanGenerator()
    parquet = generators.BooleanGenerator()
    terrace = generators.BooleanGenerator()
    balcony = generators.BooleanGenerator()
    separate_dining_room = generators.BooleanGenerator()
    living_room = generators.BooleanGenerator()
    separate_toilet = generators.BooleanGenerator()
    bathroom = generators.BooleanGenerator()
    shower = generators.BooleanGenerator()
    separate_entrance = generators.BooleanGenerator()
    cellar = generators.BooleanGenerator()
    cupboards = generators.BooleanGenerator()
    open_parking = generators.BooleanGenerator()
    box = generators.BooleanGenerator()
    #orientation = generators.ChoiceGenerator(choices = ORIENTATION_CHOICES)


class HomeForSaleAdMockup(Mockup):
    # don't follow permissions and groups
    follow_m2m = False
    factory = HomeForSaleAdFactory

    def __init__(self, *args, **kwargs):
        #self.username = kwargs.pop('username', None)
        #self.password = kwargs.pop('password', None)
        super(HomeForSaleAdMockup, self).__init__(*args, **kwargs)
        #if self.username:
        #    self.update_fieldname_generator(
        #        username = generators.StaticGenerator(self.username)
        #        )

    def unique_email(self, model, instance):
        #if User.objects.filter(email=instance.email):
        #    raise mockups.InvalidConstraint(('email',))
        pass

    def prepare_class(self):
        #self.add_constraint(self.unique_email)
        pass

    def post_process_instance(self, instance):
        if instance.nb_of_rooms < instance.nb_of_bedrooms:
            instance.nb_of_rooms = instance.nb_of_bedrooms+1
        instance.price = int(instance.price/1000) * 1000
        if instance.update_date < instance.create_date:
            instance.update_date = instance.create_date
        instance.save()
        #if instance.delete_date < instance.update_date:
        #    instance.delete_date = instance.update_date
        mo = ModeratedObject(content_object = instance, moderation_status=1)
        mo.save()
        return instance

mockups.register(HomeForSaleAd, HomeForSaleAdMockup, fail_silently=True)

