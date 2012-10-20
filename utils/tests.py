from django.test import TestCase
from utils.templatetags.utils_tags import email_local_part


class EmailToNameTest(TestCase):

    def test_email_local_part(self):
        email = "saul.goodman@breakingbad.com"
        self.assertEquals(email_local_part(email), 'saul goodman')
