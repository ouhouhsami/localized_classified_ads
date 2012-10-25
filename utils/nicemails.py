#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2009, Mathieu Agopian
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the University of California, Berkeley nor the
#       names of its contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE REGENTS AND CONTRIBUTORS ``AS IS'' AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE REGENTS AND CONTRIBUTORS BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


from os import path
from email.MIMEImage import MIMEImage
from django.core.mail import EmailMultiAlternatives
from django.template import loader, Context
from django.conf import settings


def send_nice_email(template_name,
                    email_context,
                    subject,
                    recipients,
                    from_email=None,
                    images=None,
                    fail_silently=False):
    """ Sends a multi-part e-mail with inline images with both HTML and Text.

    template_name must NOT contain an extension. Both HTML (.html) and
    TEXT (.txt) versions must exist, eg 'emails/my_nice_email' will use both
    my_nice_email.html and my_nice_email.txt.

    email_context should be a plain python dictionary. It is applied against
    both the email messages (templates) and the subject.

    subject can be plain text or a Django template string, eg:
        New Job: {{ job.id }} {{ job.title }}

    recipients can be either a string, eg 'a@b.com' or a list, eg:
        ['a@b.com', 'c@d.com']. Type conversion is done if needed.

    from_email can be an e-mail, 'Name <email>' or None. If unspecified, the
    DEFAULT_FROM_EMAIL will be used.

    images must be provided as a tuple, with the absolute path, followed by the
    image name:
        (('/path/to/image1', 'img1'), ('/path/to/image2', 'img2'))
    They are then used in the templates like the following:
        <img src="cid:img1" />

    if fail_silently is False, exceptions will be raised if an error occurs.

    Please refer to the SMTP.sendmail documentation:
        http://docs.python.org/library/smtplib.html#smtplib.SMTP.sendmail

    """

    if not from_email:
        from_email = settings.DEFAULT_FROM_EMAIL

    context = Context(email_context)

    text_part = loader.get_template('%s.txt' % template_name).render(context)
    html_part = loader.get_template('%s.html' % template_name).render(context)
    subject_part = loader.get_template_from_string(subject).render(context)

    if type(recipients) != list:
        recipients = [recipients, ]

    msg = EmailMultiAlternatives(subject_part, text_part, from_email, recipients)
    msg.mixed_subtype = 'related'
    msg.attach_alternative(html_part, 'text/html')

    if images:
        for file, name in images:
            f = open(path.join(settings.STATIC_ROOT, file), 'rb')
            msgImage = MIMEImage(f.read())
            f.close()
            msgImage.add_header('Content-ID', '<%s>' % name)
            msgImage.add_header('Content-Disposition', 'inline')
            msg.attach(msgImage)

    return msg.send(fail_silently)
