# coding=utf-8

from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
from django.contrib.sites.models import Site

from userena.forms import SignupFormOnlyEmail
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, HTML
from crispy_forms.bootstrap import FormActions


class SignupFormExtra(SignupFormOnlyEmail):
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.form_method = 'post'
        self.helper.form_action = '.'
        if Site.objects.get_current().name == 'AcheterSansCom':
            teaser_text = u"En vous inscrivant, vous pourrez : <ul>"\
                            u"<li>créer une alerte email</li>"\
                            u"<li>déposer une annonce de recherche pour être contacté directement par les vendeurs</li>"\
                            u"<li>ajouter un bien à vendre</li></ul>"
        if Site.objects.get_current().name == 'LouerSansCom':
            teaser_text = u"En vous inscrivant, vous pourrez : <ul>"\
                            u"<li>créer une alerte email</li>"\
                            u"<li>déposer une demande de location pour être contacté directement par les propriétaires</li>"\
                            u"<li>ajouter un bien à louer</li></ul>"
        teaser_text = '<div class="alert alert-info">'+teaser_text+'</div>'
        self.helper.layout = Layout(
            Fieldset(
                _(u'S\'inscrire'),
                HTML(teaser_text),
                'email',
                'password1',
                'password2'
            ),
            FormActions(
                Submit('submit', _(u'S\'inscrire'), css_class='btn btn-primary')
            )
        )
        super(SignupFormExtra, self).__init__(*args, **kwargs)

    def clean_email(self):
        """ Validate that the e-mail address is unique. """
        if User.objects.filter(email__iexact=self.cleaned_data['email']):
            error_msg = _(u'Un compte existe déjà avec cette adresse électronique. \
                Si c\'est la votre <a href="%s" >connectez-vous</a>, sinon inscrivez-vous avec une autre adresse électronique.' % (reverse('userena_signup')))
            error_msg = mark_safe(error_msg)
            raise forms.ValidationError(error_msg)
        return self.cleaned_data['email']
