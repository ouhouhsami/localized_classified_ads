from django.db import models
from django.contrib.gis.db import models
from userena.models import UserenaBaseProfile

class UserProfile(UserenaBaseProfile):
    """User profile model

    """
    #birthdate		= models.DateField(null = True, blank = True)
    phone_number	= models.CharField(max_length=255, null = True, blank = True)
    location		= models.PointField(default='POINT(-95.3385 29.7245)', srid=900913)
    #user 			= models.ForeignKey(User, unique=True)

    objects = models.GeoManager()
    
    def __unicode__(self):
        return "%s" % (self.user)

'''
    def get_absolute_url(self):
        return ('profiles_profile_detail', (), { 'username': self.user.username })
    get_absolute_url = models.permalink(get_absolute_url)   
'''