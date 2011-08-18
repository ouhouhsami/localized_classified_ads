# coding=utf-8
from django.db import models
from django.contrib.gis.db import models
from userena.models import UserenaBaseProfile

class UserProfile(UserenaBaseProfile):
    """User profile model

    """
    phone_number	= models.CharField("Numéro de téléphone", max_length=255, null = True, blank = True)
    email_alert		= models.BooleanField("Recevoir les alertes email pour vos recherches")
    #location		= models.PointField(default='POINT(261278.51676999778 6250645.2903766)', srid=900913)
    #objects = models.GeoManager()