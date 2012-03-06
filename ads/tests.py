# coding=utf-8
from django.utils import unittest
from ads.models import Ad


class TestAd(Ad):
    pass

class TestAdForm(object):
    pass

class TestAdFilterSet(object):
    pass

class AdTestCase(unittest.TestCase):
    def test_home(self):
        pass


