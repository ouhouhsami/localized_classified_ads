from crispy_forms.layout import Field, Fieldset
from crispy_forms.utils import render_field

from django.template.loader import render_to_string
from django.template import Context, Template

class AppendedPrependedText(Field):
    template = "bootstrap/layout/appended_prepended_text.html"
   
    def __init__(self, field, prepended_text, appended_text, *args, **kwargs):
        self.appended_text = appended_text
        self.prepended_text = prepended_text
        if 'active' in kwargs:
            self.active = kwargs.pop('active')

        super(AppendedPrependedText, self).__init__(field, *args, **kwargs)

    def render(self, form, form_style, context):
        context.update({'crispy_appended_text': self.appended_text, 
                        'crispy_prepended_text': self.prepended_text,
                        'active': getattr(self, "active", False)})
        return render_field(self.field, form, form_style, context, template=self.template, attrs=self.attrs)

class MultiField(object):
    """ multiField container. Renders to a multiField <div> """
    template = "bootstrap/layout/multifield.html"

    def __init__(self, label, *fields, **kwargs):
        #TODO: Decide on how to support css classes for both container divs
        self.fields = fields
        self.label_html = unicode(label)
        self.label_class = kwargs.get('label_class', u'blockLabel')
        self.css_class = kwargs.get('css_class', u'ctrlHolder')
        self.css_id = kwargs.get('css_id', None)
        self.template = kwargs.get('template', self.template)

    def render(self, form, form_style, context):
        if form.errors:
            self.css_class += " error"

        # We need to render fields using django-uni-form render_field so that MultiField can
        # hold other Layout objects inside itself
        fields_output = u''
        self.bound_fields = []
        for field in self.fields:
            fields_output += render_field(field, form, form_style, context, 'bootstrap/multifield.html', self.label_class, layout_object=self)
        return render_to_string(self.template, Context({'multifield': self, 'fields_output': fields_output}))

class BootstrapFieldset(Fieldset):

    template = "bootstrap/layout/fieldset.html"

    def __init__(self, legend, *fields, **kwargs):
        self.fields = list(fields)
        self.legend = unicode(legend)
        self.css_class = kwargs.get('css_class', '')
        self.css_id = kwargs.get('css_id', None)
        self.collapse_in = kwargs.get('collapse_in', False)
        # Overrides class variable with an instance level variable
        self.template = kwargs.get('template', self.template)

    def set_collapse(self, value):
        self.collapse_in = value