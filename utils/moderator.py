from moderation.moderator import GenericModerator


class AdModerator(GenericModerator):
    fields_exclude = ['update_date', 'create_date', 'delete_date']
    notify_moderator = True
    notify_user = True
    visibility_column = 'visible'
