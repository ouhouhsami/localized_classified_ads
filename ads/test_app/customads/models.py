from django.db import models
from ads.models import Ad

class TestAd(Ad):
    brand = models.CharField(max_length=255, null=True, blank=True)