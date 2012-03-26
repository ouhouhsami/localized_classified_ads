# coding=utf-8
""" ads test module"""

from django.utils import unittest
from django.test.client import Client

from ads.models import Ad

"""
TODO: test if mail is sent to user for moderation
"""

class TestAd(Ad):
    pass

class TestAdForm(object):
    pass

class TestAdFilterSet(object):
    pass

class AdTestCase(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_searchview(self):
        """Test that home page is reachable"""
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)


