#-*- coding: utf-8 -*-
from geoads.forms import AdContactForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Div
from crispy_forms.bootstrap import Field


class HomeContactForm(AdContactForm):
    """
    Base contact form
    """
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_class = 'form'
        self.helper.form_method = 'post'
        self.helper.form_action = ''
        self.helper.form_tag = False
        self.helper.html5_required = True
        self.helper.layout = Layout(
            Fieldset('Contacter le vendeur',
                Div(Field('message', css_class="span4"))
            )
        )
        super(HomeContactForm, self).__init__(*args, **kwargs)
