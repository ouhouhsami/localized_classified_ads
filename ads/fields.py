# coding=utf-8
from django import forms
import floppyforms as forms

class PriceField(forms.Field):
    def to_python(self, value):
        """Normalize data to price field"""
        try:
            return int(str(value).replace('.', '').replace(' ', '').replace(',', ''))
        except:
            raise forms.ValidationError("Entrez un prix en euros.")

class SurfaceField(forms.Field):
    def to_python(self, value):
        """Normalize data to surface field"""
        if not value:
            #print 'null value'
            return None
        try:
            return round(float(str(value).replace(',', '.')))
        except:
            raise forms.ValidationError("Entrez une surface en mètre carré.")