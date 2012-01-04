from moderation import moderation
from models import HomeForRentAd
from ads.moderator import AdModerator

moderation.register(HomeForRentAd, AdModerator)