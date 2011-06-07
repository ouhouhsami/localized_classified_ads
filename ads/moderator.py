from moderation import moderation
from ads.models import *
from moderation.moderator import GenericModerator
from moderation.managers import ModerationObjectsManager
from django.contrib.gis.db import models


class HomeForSaleAdModerator(GenericModerator):
    fields_exclude = ['update_date', 'create_date', 'delete_date']
    #auto_approve_for_superusers = False
    # manager_names = ['objects']
    # moderation_manager_class = ModerationObjectsManager
    notify_moderator = True
    notify_user = True

moderation.register(HomeForSaleAd, HomeForSaleAdModerator)