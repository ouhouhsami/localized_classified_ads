from ads.filtersets import AdFilterSet
from ads.test_app.customads.models import TestAd
from ads.test_app.customads.forms import TestAdFilterSetForm

class TestAdFilterSet(AdFilterSet):
    class Meta:
        model = TestAd
        form = TestAdFilterSetForm
        fields = ['brand']