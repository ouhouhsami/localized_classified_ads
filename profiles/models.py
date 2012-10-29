#-*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings

from userena.models import UserenaBaseProfile, UserenaSignup
from userena.utils import get_protocol
from userena import settings as userena_settings

from homeads.mails import UserSignIn


class HomeAdSignUp(UserenaSignup):

    def send_activation_email(self):
        """
        Sends a activation email to the user.

        This email is send when the user wants to activate their newly created
        user.
        Override default userena mechanism, to send beautiful HTML email
        """
        email_context = {'user': self.user,
                  'without_usernames': userena_settings.USERENA_WITHOUT_USERNAMES,
                  'protocol': get_protocol(),
                  'activation_days': userena_settings.USERENA_ACTIVATION_DAYS,
                  'activation_key': self.activation_key, 'to': self.user.email}

        msg = UserSignIn(email_context, self.user.email)
        msg.send()

    def send_confirmation_email(self):
        # TODO !!!!!!!!!
        context = {'user': self.user,
                  'without_usernames': userena_settings.USERENA_WITHOUT_USERNAMES,
                  'new_email': self.email_unconfirmed,
                  'protocol': get_protocol(),
                  'confirmation_key': self.email_confirmation_key,
                  'site': Site.objects.get_current()}
        # Email to the old address, if present
        subject_old = render_to_string('userena/emails/confirmation_email_subject_old.txt',
                                       context)
        subject_old = ''.join(subject_old.splitlines())

        message_old = render_to_string('userena/emails/confirmation_email_message_old.txt',
                                       context)
        if self.user.email:
            send_mail(subject_old,
                      message_old,
                      settings.DEFAULT_FROM_EMAIL,
                    [self.user.email])
        # Email to the new address
        subject_new = render_to_string('userena/emails/confirmation_email_subject_new.txt',
                                       context)
        subject_new = ''.join(subject_new.splitlines())

        message_new = render_to_string('userena/emails/confirmation_email_message_new.txt',
                                       context)

        send_mail(subject_new,
                  message_new,
                  settings.DEFAULT_FROM_EMAIL,
                  [self.email_unconfirmed, ])

    class Meta:
        db_table = 'userena_userenasignup'


class UserProfile(UserenaBaseProfile):
    """
    User profile model
    """
    user = models.OneToOneField(User,
                                unique=True,
                                verbose_name='user',
                                related_name='my_profile')
    phone_number = models.CharField("Numéro de téléphone", max_length=255, null=True, blank=True)
