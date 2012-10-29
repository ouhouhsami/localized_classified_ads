#-*- coding: utf-8 -*-
from moderation.moderator import GenericModerator
from utils.managers import ModeratedAdManager


class AdModerator(GenericModerator):
    fields_exclude = ['update_date', 'create_date', 'delete_date']
    notify_moderator = True
    notify_user = True
    visibility_column = 'visible'
    moderation_manager_class = ModeratedAdManager  # allow geomanager + moderationmanager
