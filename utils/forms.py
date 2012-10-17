from geoads.forms import BaseAdForm, AdContactForm
from moderation.forms import BaseModeratedObjectForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Fieldset, ButtonHolder, Div, HTML
from crispy_forms.bootstrap import FormActions, AppendedText, PrependedText, Field


class BaseModeratedAdForm(BaseModeratedObjectForm, BaseAdForm):
    pass


class HomeContactForm(AdContactForm):
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
