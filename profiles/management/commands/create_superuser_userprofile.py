from django.core.management.base import BaseCommand, CommandError
from profiles.models import UserProfile
from django.contrib.auth.models import User

class Command(BaseCommand):

    def handle(self, *args, **options):
        user = User.objects.get(id=1)
        up =  UserProfile(user = user, privacy='open')
        up.save()