import random
import factory
from pygeocoder import Geocoder

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.gis.geos import Point

from geoads.models import Ad, AdSearch

from models import HomeForSaleAd


ADDRESSES = ["13 Place d'Aligre, Paris",
    "22 rue Esquirol, Paris",
    "1 Avenue des Aqueducs, Arcueil",
    "1 place du Chatelet, Paris", ]


class UserFactory(factory.Factory):
    FACTORY_FOR = User

    username = factory.Sequence(lambda n: "user_%s" % n)
    email = factory.LazyAttribute(lambda o: '%s@example.org' % o.username)
    #password = factory.declarations.PostGenerationMethodCall('set_password', password='password')

    @classmethod
    def _prepare(cls, create, password=None, **kwargs):
        return super(UserFactory, cls)._prepare(
            create,
            password=make_password(password),
            **kwargs
        )


class BaseAdFactory(factory.Factory):
    FACTORY_FOR = Ad

    user_entered_address = random.choice(ADDRESSES)
    user = factory.SubFactory(UserFactory)

    @classmethod
    def _prepare(cls, create, **kwargs):
        user_entered_address = kwargs['user_entered_address']
        #try:
        #    geocode = Geocoder.geocode(user_entered_address.encode('ascii',
        #        'ignore'))
        #    coordinates = geocode[0].coordinates
        #    location = str(Point(coordinates[1], coordinates[0], srid=900913))
        #except:
        location = 'POINT (2.3316097000000000 48.8002050999999994)'
        test_ad = super(BaseAdFactory, cls)._prepare(create, location=location,
            **kwargs)
        return test_ad


class HomeForSaleAdFactory(BaseAdFactory):
    FACTORY_FOR = HomeForSaleAd

    price = random.randint(10000, 2000000)
    surface = random.randint(8, 350)
    nb_of_rooms = random.randint(1, 15)
    nb_of_bedrooms = random.randint(0, 10)


class HomeForSaleAdSearchFactory(factory.Factory):
    FACTORY_FOR = AdSearch

    user = factory.SubFactory(UserFactory)
    #content_type = ContentType.objects.get_for_model(HomeForSaleAd)
    #ouf: content_type is bypassed !
