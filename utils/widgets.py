# coding=utf-8

from geoads.widgets import SpecificRangeWidget
import floppyforms as forms

class AppendTextInput(forms.TextInput):
    template_name = 'floppyforms/append_text_input.html'

class BootstrapSpecificRangeWidget(forms.MultiWidget):
    """
    Specific Range Widget, a range widget with min and max inputs
    """
    def __init__(self, attrs=None, appended_text=None):
        widgets = (forms.TextInput(attrs={'placeholder':'min', 'class':'input-mini', 'appended_text':appended_text}),
                   AppendTextInput(attrs={'placeholder':'max', 'class':'input-mini', 'appended_text':appended_text}))
        super(BootstrapSpecificRangeWidget, self).__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            return [value.start, value.stop]
        return [None, None]

    def format_output(self, rendered_widgets):
        return u' - '.join(rendered_widgets)