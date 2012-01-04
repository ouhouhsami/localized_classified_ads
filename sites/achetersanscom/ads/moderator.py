from moderation import moderation
from models import HomeForSaleAd
from ads.moderator import AdModerator

moderation.register(HomeForSaleAd, AdModerator)