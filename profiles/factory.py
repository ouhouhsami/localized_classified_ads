# -*- coding: utf-8 -*-
import mockups
from datetime import datetime
from models import UserProfile
from mockups import Mockup, Factory
from mockups import generators
from django.contrib.auth.models import User
from moderation.models import ModeratedObject
import string
import random

class UserProfileFactory(Factory):
    pass

class UserProfileMockup(Mockup):
    # don't follow permissions and groups
    follow_m2m = False
    # generate_fk= False
    factory = UserProfileFactory
    def post_process_instance(self, instance):
        instance.user.username = ''.join((random.choice(string.letters+string.digits) for _ in xrange(random.randint(5,8))))
        instance.user.save()

mockups.register(UserProfile, UserProfileMockup, fail_silently=True)
