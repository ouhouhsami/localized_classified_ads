# coding=utf-8

from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.dispatch import receiver
from django.core.mail import send_mail
from django.contrib.sites.models import Site
from django.contrib.contenttypes.models import ContentType
from django.views.generic import DetailView

from moderation.models import ModeratedObject
from userena.signals import signup_complete, activation_complete
from ads.models import AdSearch

from profiles.models import UserProfile


class UserProfileDetailView(DetailView):
    """
    UserProfile detail view
    """
    model = UserProfile
    ad_model = None
    template_name = 'profiles/profile.html'
    context_object_name = 'profile'
    slug_field = 'user__username'

    def get_context_data(self, *args, **kwargs):
        context = super(UserProfileDetailView, self).get_context_data(**kwargs)
        context['ads'] = self.ad_model.objects.exclude(delete_date__isnull = False)\
                    .filter(user_profile = self.get_object())\
                    .order_by('-create_date')
        context['all_user_ads'] = False
        context['searchs'] = False
        if self.request.user ==  self.get_object().user:
            context['all_user_ads'] = self.ad_model.unmoderated_objects.filter(user_profile = self.get_object())\
                         .exclude(delete_date__isnull = False)\
                         .order_by('-create_date')
            context['searchs'] = AdSearch.objects.filter(user_profile = self.get_object(), 
                            content_type=ContentType.objects.get_for_model(self.ad_model))
        return context

@receiver(signup_complete)
def signup_complete_callback(sender, **kwargs):
    send_mail('[%s] Nouvelle inscription : %s' % (Site.objects.get_current().name, kwargs['user'].email), "", 'contact@achetersanscom.com', ["contact@achetersanscom.com"], fail_silently=False)


@receiver(activation_complete)
def activation_complete_callback(sender, **kwargs):
    send_mail('[%s] Inscription validee : %s' % (Site.objects.get_current().name, kwargs['user'].email), "", 'contact@achetersanscom.com', ["contact@achetersanscom.com"], fail_silently=False)

