
#from moderation.forms import BaseModeratedObjectForm
from django.forms import ModelForm

from ads.forms import BaseAdForm
from ads.test_app.customads.models import TestAd

class TestAdForm(BaseAdForm):
    class Meta:
        model = TestAd
        exclude = ('user', 'delete_date', 'location', 'address')

class TestAdFilterSetForm(ModelForm):
    class Meta:
        model = TestAd
        exclude = ('user', 'delete_date', 'location', 'address')