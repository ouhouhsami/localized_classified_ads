# coding=utf-8

from django import forms
from django.forms import ModelForm
from django.utils.safestring import mark_safe
from django.contrib.gis.geos import Point

from pygeocoder import Geocoder, GeocoderError
from ads.models import AdPicture, AdContact

class ImageWidget(forms.FileInput):
    template = '%(input)s<br /><a href="%(image)s" target="_blank"><img src="%(image_thumbnail)s" /></a>'

    def __init__(self, attrs=None, template=None, width=200, height=200):
        if template is not None:
            self.template = template
        self.width = width
        self.height = height
        super(ImageWidget, self).__init__(attrs)

    def render(self, name, value, attrs=None):
        input_html = super(forms.FileInput, self).render(name, value, attrs)
        if hasattr(value, 'width') and hasattr(value, 'height'):
            output = self.template % {'input': input_html, 'image': value.url,
                                      'image_thumbnail': value.thumbnail.url()}
        else:
            output = input_html
        return mark_safe(output)

class AdPictureForm(ModelForm):
    image = forms.ImageField(widget=ImageWidget(), required=False)
    class Meta:
        model = AdPicture

class AdContactForm(ModelForm):
    class Meta:
        model = AdContact
        exclude = ['user', 'content_type', 'object_pk']

class BaseAdForm(ModelForm):

    def clean(self):
        if self.cleaned_data.has_key('user_entered_address'):
            self.cleaned_data['address'] = self.address
            self.cleaned_data['location'] = self.location
        return self.cleaned_data

    def clean_user_entered_address(self):
        data = self.cleaned_data['user_entered_address']
        try:
            geocode = Geocoder.geocode(data.encode('ascii','ignore'))
            self.address = geocode.raw
            coordinates = geocode[0].coordinates
            pnt = Point(coordinates[1], coordinates[0], srid=900913)
            self.location = pnt
        except GeocoderError:
            raise forms.ValidationError(u"Indiquer une adresse valide")
        return data

