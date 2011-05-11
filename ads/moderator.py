from moderation import moderation
from ads.models import *
from moderation.moderator import GenericModerator
from moderation.managers import ModerationObjectsManager
from django.contrib.gis.db import models


class HomeForSaleAdModerator(GenericModerator):
    fields_exclude = ['update_date', 'create_date', 'delete_date']
    # manager_names = ['objects']
    # moderation_manager_class = ModerationObjectsManager

moderation.register(HomeForSaleAd, HomeForSaleAdModerator)