import datetime
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.core.management.base import BaseCommand, CommandError
from django.http import QueryDict
from django.template.loader import render_to_string
from profiles.models import UserProfile
from ads.models import HomeForSaleAd, HomeForSaleSearch
from ads.filtersets import HomeForSaleAdFilterSet
from moderation.models import ModeratedObject

class Command(BaseCommand):

    def handle(self, *args, **options):
        user_profiles = UserProfile.objects.all()
        for user_profile in user_profiles:
            research = HomeForSaleSearch.objects.filter(user_profile = user_profile)
            for home_for_sale_search in research:
                q = QueryDict(home_for_sale_search.search)
                filter = HomeForSaleAdFilterSet(q or None, search = False)
                ads = filter.qs
                '''
                for ad in filter.qs:
                    if ad.update_date.date() == datetime.date.today():
                        ads.append(ad)
                        # add moderation ok
                    # impossible d'avoir acces a la moderation
                    # moderation_object = ModeratedObject(content_object = ad)
                    # print moderation_object
                '''
                if len(ads) > 0:
                    subject = render_to_string('profiles/email_alert_subject.html', { 'search': home_for_sale_search })
                    content = render_to_string('profiles/email_alert.html', { 'ads': ads })
                    send_mail(subject, content, 'contact@achetersanscom.com',
                              [user_profile.user.email], fail_silently=False)