from django.core.management.base import BaseCommand, CommandError
from profiles.factory import UserProfileMockup
from profiles.models import UserProfile

class Command(BaseCommand):

    def handle(self, *args, **options):
        mockup = UserProfileMockup(UserProfile)
        entries = mockup.create(100)       