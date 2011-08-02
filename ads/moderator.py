from moderation import moderation
from ads.models import *
from moderation.moderator import GenericModerator
from moderation.managers import ModerationObjectsManager
from django.contrib.gis.db import models


class HomeForSaleAdModerator(GenericModerator):
    fields_exclude = ['update_date', 'create_date', 'delete_date']
    # auto_approve_for_superusers = False
    # manager_names = ['objects']
    # moderation_manager_class = ModerationObjectsManager
    notify_moderator = True
    notify_user = True


    def inform_moderator(self, content_object, extra_context=None):
        extra_context={'test':'test'}
        super(HomeForSaleAdModerator, self).inform_moderator(content_object,
                                                           extra_context)


    def inform_user(self, content_object, user, extra_context=None):
        print 'teste'
        extra_context={'test':'test'}
        super(HomeForSaleAdModerator, self).inform_user(content_object,user,extra_context)

moderation.register(HomeForSaleAd, HomeForSaleAdModerator)