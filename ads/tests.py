from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.conf import settings
from django.contrib.auth.models import User

from profiles.models import UserProfile
from ads.models import HomeForSaleAd

class HomeTestCase(TestCase):

    def setUp(self):
        self.c = Client(SERVER_NAME="www.achetersanscom.com")

    def test_search_index(self):
        """Test that home page is reachable"""
        resp = self.c.get('/')
        self.assertEqual(resp.status_code, 200)

    def test_search_index_latest_ads(self):
        """Test that pending or rejected latest ads don't appear in home page
        and approved ones appear.
        """
        user = User.objects.create_user('urbania', 'urbania@arnaqueur.com', 'soushomme')
        user_profile = UserProfile(user=user)
        user_profile.save()
        home = HomeForSaleAd(user_profile=user_profile, 
                             price="624000", habitation_type="0", 
                             surface="63", nb_of_rooms="3", 
                             location="POINT (264809.3316514802863821 6249274.9133867248892784)", 
                             nb_of_bedrooms="2")
        home.save()
        resp = self.c.get('/')
        self.assertEqual(len(resp.context['initial_ads']), 0)
        home.moderated_object.approve()
        resp = self.c.get('/')
        self.assertEqual(resp.context['initial_ads'][0], home)
        home.moderated_object.reject()
        resp = self.c.get('/')
        self.assertEqual(len(resp.context['initial_ads']), 0)

class AddAdTestCase(TestCase):

    def setUp(self):
        self.c = Client(SERVER_NAME="www.achetersanscom.com")

    def test_add_ad_page_notlogged(self):
        """Test that not logged users can't add an ad"""
        resp = self.c.get(reverse('add'))
        self.assertEqual(resp.status_code, 302)

    def test_add_ad_page_logged(self):
        """Test that logged users can add an ad"""
        user = User.objects.create_user('urbania', 'urbania@arnaqueur.com', 'soushomme')
        user_profile = UserProfile(user=user)
        user_profile.save()
        self.c.login(username='urbania', password='soushomme')
        resp = self.c.get(reverse('add'))
        self.assertEqual(resp.status_code, 200)

    def test_post_new_add(self):
        """Test the creation of an add by a logged user"""
        user = User.objects.create_user('urbania', 'urbania@arnaqueur.com', 'soushomme')
        user_profile = UserProfile(user=user)
        user_profile.save()
        self.c.login(username='urbania', password='soushomme')
        #resp = self.c.get(reverse('add'))
        ad_home = {'user_profile':user_profile, 'price':624000, 
                   'habitation_type':"0", 'surface':63, 'nb_of_rooms':3, 
                   'location':"POINT (264809.3316514802863821 6249274.9133867248892784)", 
                   'nb_of_bedrooms':2}
        resp = self.c.post(reverse('add'), ad_home)
        #print resp
        print HomeForSaleAd.objects.all()
        #self.assertEqual(resp.status_code, 200)
