from datetime import datetime

from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from django.http import QueryDict
from django.template.loader import render_to_string

from profiles.models import UserProfile
from geoads.models import AdSearch
from sites.achetersanscom.ads.filtersets import HomeForSaleAdFilterSet
from sites.louersanscom.ads.filtersets import HomeForRentAdFilterSet


class Command(BaseCommand):
    """
    Send alert email for user research, based on current date
    (could be run by a cronjob)
    """
    def handle(self, *args, **options):
        user_profiles = UserProfile.objects.all()
        for user_profile in user_profiles:
            research = AdSearch.objects.filter(user=user_profile.user)
            for item in research:
                if item.content_type.model == 'homeforsalead':
                    site_name = 'AcheterSansCom'
                    ad_filterset = HomeForSaleAdFilterSet
                elif item.content_type.model == 'homeforrentad':
                    site_name = 'LouerSansCom'
                    ad_filterset = HomeForRentAdFilterSet
                q = QueryDict(item.search)
                filter = ad_filterset(q or None, search=False)
                ads = filter.qs\
                            .filter(update_date__year=datetime.now().year)\
                            .filter(update_date__month=datetime.now().month)\
                            .filter(update_date__day=datetime.now().day)
                if len(ads) > 0:
                    subject = render_to_string('profiles/email_alert_subject.html',
                                                          {'site_name': site_name})
                    content = render_to_string('profiles/email_alert_message.html',
                                                          {'site_name': site_name,
                                                           'ads': ads,
                                                           'search': item,
                                                           'user_profile': user_profile})
                    send_mail(subject, content, 'contact@%s.com' % (site_name.lower()),
                              [user_profile.user.email], fail_silently=False)
