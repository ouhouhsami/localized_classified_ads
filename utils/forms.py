#-*- coding: utf-8 -*-
from django.forms import ModelForm

from geoads.forms import BaseAdForm
from geoads.models import AdPicture
from moderation.forms import BaseModeratedObjectForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, HTML
from crispy_forms.bootstrap import Field

import floppyforms as forms


class BaseModeratedAdForm(BaseModeratedObjectForm, BaseAdForm):
    """
    Base Moderated Ad Form
    """
    pass


class PrettyAdPictureForm(ModelForm):
    """
    Pretty Ad Picture Form
    """
    image = forms.ImageField(widget=forms.FileInput, required=False)

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Div(
                #HTML(u'<button type="button" class="close" data-dismiss="alert">×</button> <h4>Photo n°{{ forloop.counter }}</h4>'),
                HTML(u'<h4>Photo n°{{ forloop.counter }}</h4>'),
                Layout(
                    Div(
                        Field('image', template="crispy_forms/no_label_field.html"),
                        Field('title', placeholder="Description", template="crispy_forms/no_label_field.html"),
                        Field('DELETE', template="crispy_forms/no_label_field.html"),
                        css_class="pull-left"
                    )
                ),
                css_class="alert alert-info clearfix", style="background-color:#fff;"
            ),
        )
        super(PrettyAdPictureForm, self).__init__(*args, **kwargs)
        if self.instance.image:
            html = "<div class='thumbnail'><img src='%s' width='350px' ></div>" % (self.instance.image.url)
            self.helper.layout.fields[0].fields[1].fields.append(Div(HTML(html), css_class="pull-right"))

    class Meta:
        model = AdPicture
