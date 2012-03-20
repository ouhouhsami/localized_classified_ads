from datetime import datetime
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.core.management.base import BaseCommand, CommandError
from django.http import QueryDict
from django.template.loader import render_to_string
from profiles.models import UserProfile
from ads.models import AdSearch, Ad
from sites.achetersanscom.ads.filtersets import HomeForSaleAdFilterSet
from sites.louersanscom.ads.filtersets import HomeForRentAdFilterSet
from moderation.models import ModeratedObject
from django.conf import settings


class Command(BaseCommand):
    """
    Send alert email for user reseach, based on current date (could be run by a cronjob)
    """
    def handle(self, *args, **options):
        #print settings.PER_SITE_OBJECTS
        user_profiles = UserProfile.objects.all()
        for user_profile in user_profiles:
            research = AdSearch.objects.filter(user = user_profile.user)
            for item in research:
                if item.content_type.model == 'homeforsalead':
                    current_context = settings.PER_SITE_OBJECTS['AcheterSansCom']
                elif item.content_type.model == 'homeforrentad':
                    current_context = settings.PER_SITE_OBJECTS['LouerSansCom']
                q = QueryDict(item.search)
                filter = current_context['ad_filterset'](q or None, search = False)
                ads = filter.qs.filter(update_date__year = datetime.now().year).filter(update_date__month = datetime.now().month).filter(update_date__day = datetime.now().day)
                #ads = filter.qs
                if len(ads) > 0:
                    #print ads
                    subject = render_to_string('profiles/email_alert_subject.html', {'site_name': current_context['site_name'] })
                    content = render_to_string('profiles/email_alert_message.html', {'site_name': current_context['site_name'], 'ads': ads, 'search': item, 'user_profile':user_profile  })
                    #print content
                    send_mail(subject, content, 'contact@%s.com' % (current_context['site_name'].lower()),
                              [user_profile.user.email], fail_silently=False)
                