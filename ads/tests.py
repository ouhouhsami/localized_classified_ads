from django.test import TestCase

class SearchTestCase(TestCase):
    def test_search_index(self):
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)  