from moderation import moderation
from models import HomeForRentAd
from utils.moderator import AdModerator

moderation.register(HomeForRentAd, AdModerator)