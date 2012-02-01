from moderation import moderation
from moderation.moderator import GenericModerator
from moderation.managers import ModerationObjectsManager

from django.contrib.gis.db import models


class AdModerator(GenericModerator):
    fields_exclude = ['update_date', 'create_date', 'delete_date']
    notify_moderator = True
    notify_user = True
    visibility_column = 'visible'



