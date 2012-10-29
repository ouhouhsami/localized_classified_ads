#-*- coding: utf-8 -*-
from os import path

from django.core.mail import EmailMultiAlternatives
from django.contrib.sites.models import Site
from django.conf import settings
from django.template import loader, Context
from email.MIMEImage import MIMEImage


class AdEmailMultiAlternatives(EmailMultiAlternatives):

    default_images = None
    default_context = None
    template_name = None
    subject = None

    def __init__(self, email_context, recipients, sender=None,
        email_images=()):
        if not sender:
            sender = settings.DEFAULT_FROM_EMAIL
        context = Context(dict(self.get_default_context().items() +
            email_context.items() +
            {'site': Site.objects.get_current()}.items()))
        images = self.get_default_images() + email_images
        text_part = loader.get_template('%s.txt' %\
            self.template_name).render(context)
        html_part = loader.get_template('%s.html' %\
            self.template_name).render(context)
        subject_part = loader.get_template_from_string(self.subject)\
            .render(context)
        if type(recipients) != list:
            recipients = [recipients, ]
        super(AdEmailMultiAlternatives, self).__init__(subject_part, text_part,
            sender, recipients)
        self.mixed_subtype = 'related'
        self.attach_alternative(html_part, 'text/html')

        if images:
            for file, name in images:
                f = open(path.join(settings.STATIC_ROOT, file), 'rb')
                msgImage = MIMEImage(f.read())
                f.close()
                msgImage.add_header('Content-ID', '<%s>' % name)
                msgImage.add_header('Content-Disposition', 'inline')
                self.attach(msgImage)

    def get_default_context(self):
        if self.default_context is None:
            return {}

    def get_default_images(self):
        if self.default_files is None:
            return ()

