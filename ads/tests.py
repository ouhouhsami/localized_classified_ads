import re

from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.conf import settings
from django.contrib.auth.models import User
from django.core import mail
from django.core.management import call_command

from moderation.models import ModeratedObject

from profiles.models import UserProfile
from ads.models import HomeForSaleAd
from ads.forms import HomeForSaleAdForm
from ads.filtersets import HomeForSaleAdFilterSet

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
                             #address="[{u'long_name': u'13', u'short_name': u'13', u'types': [u'street_number']}, {u'long_name': u'Place d Aligre', u'short_name': u'Place d Aligre', u'types': [u'route']}, {u'long_name': u'12\xe8me Arrondissement Paris', u'short_name': u'12\xe8me Arrondissement Paris', u'types': [u'sublocality', u'political']}, {u'long_name': u'Paris', u'short_name': u'Paris', u'types': [u'locality', u'political']}, {u'long_name': u'Paris', u'short_name': u'75', u'types': [u'administrative_area_level_2', u'political']}, {u'long_name': u'\xcele-de-France', u'short_name': u'IdF', u'types': [u'administrative_area_level_1', u'political']}, {u'long_name': u'France', u'short_name': u'FR', u'types': [u'country', u'political']}, {u'long_name': u'75012', u'short_name': u'75012', u'types': [u'postal_code']}]",
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

    def test_add_delete_notlogged(self):
        """Test that not logged users can't delete an ad"""
        user = User.objects.create_user('urbania', 'urbania@arnaqueur.com', 'soushomme')
        user_profile = UserProfile(user=user)
        user_profile.save()       
        home = HomeForSaleAd(user_profile=user_profile, 
                             price="624000", habitation_type="0", 
                             surface="63", nb_of_rooms="3", 
                             location="POINT (264809.3316514802863821 6249274.9133867248892784)", 
                             #address="[{u'long_name': u'13', u'short_name': u'13', u'types': [u'street_number']}, {u'long_name': u'Place d Aligre', u'short_name': u'Place d Aligre', u'types': [u'route']}, {u'long_name': u'12\xe8me Arrondissement Paris', u'short_name': u'12\xe8me Arrondissement Paris', u'types': [u'sublocality', u'political']}, {u'long_name': u'Paris', u'short_name': u'Paris', u'types': [u'locality', u'political']}, {u'long_name': u'Paris', u'short_name': u'75', u'types': [u'administrative_area_level_2', u'political']}, {u'long_name': u'\xcele-de-France', u'short_name': u'IdF', u'types': [u'administrative_area_level_1', u'political']}, {u'long_name': u'France', u'short_name': u'FR', u'types': [u'country', u'political']}, {u'long_name': u'75012', u'short_name': u'75012', u'types': [u'postal_code']}]",
                             nb_of_bedrooms="2")
        home.save()
        home.moderated_object.approve()
        user2 = User.objects.create_user('urbania2', 'urbania2@arnaqueur.com', 'soushomme2')
        user_profile2 = UserProfile(user=user2)
        user_profile2.save()
        resp = self.c.get(reverse('delete', kwargs={'ad_id': home.id}))
        self.assertEqual(resp.status_code, 302)
        self.c.login(username='urbania2', password='soushomme2')
        resp = self.c.get(reverse('delete', kwargs={'ad_id': home.id}))
        self.assertEqual(HomeForSaleAd.objects.all()[0], home)
        self.c.login(username='urbania', password='soushomme')
        resp = self.c.get(reverse('delete', kwargs={'ad_id': home.id}))
        self.assertEqual(HomeForSaleAd.objects.all().count(), 0)

    def test_add_ad_page_logged(self):
        """Test that logged users can add an ad"""
        user = User.objects.create_user('urbania', 'urbania@arnaqueur.com', 'soushomme')
        user_profile = UserProfile(user=user)
        user_profile.save()
        self.c.login(username='urbania', password='soushomme')
        resp = self.c.get(reverse('add'))
        self.assertEqual(resp.status_code, 200)

    def test_add_create_udpate_delete(self):
        """Test the creation of an add by a logged user"""
        user = User.objects.create_user('urbania', 'urbania@arnaqueur.com', 'soushomme')
        user_profile = UserProfile(user=user)
        user_profile.save()
        self.c.login(username='urbania', password='soushomme')
        # below important things in post : 'ads-adpicture-content_type-object_id-TOTAL_FORMS'
        # and 'ads-adpicture-content_type-object_id-INITIAL_FORMS'
        # value got from PictureFormset.get_default_prefix()
        ad_home = {'user_profile':user_profile, 'price':624000, 
                   'habitation_type':"0", 'surface':63, 'nb_of_rooms':3, 
                   'location':"POINT (264809.3316514802863821 6249274.9133867248892784)", 
                   'address':"[{u'long_name': u'13', u'short_name': u'13', u'types': [u'street_number']}, {u'long_name': u'Place d Aligre', u'short_name': u'Place d Aligre', u'types': [u'route']}, {u'long_name': u'12\xe8me Arrondissement Paris', u'short_name': u'12\xe8me Arrondissement Paris', u'types': [u'sublocality', u'political']}, {u'long_name': u'Paris', u'short_name': u'Paris', u'types': [u'locality', u'political']}, {u'long_name': u'Paris', u'short_name': u'75', u'types': [u'administrative_area_level_2', u'political']}, {u'long_name': u'\xcele-de-France', u'short_name': u'IdF', u'types': [u'administrative_area_level_1', u'political']}, {u'long_name': u'France', u'short_name': u'FR', u'types': [u'country', u'political']}, {u'long_name': u'75012', u'short_name': u'75012', u'types': [u'postal_code']}]",
                   'nb_of_bedrooms':2,'ads-adpicture-content_type-object_id-TOTAL_FORMS':1, 
                   'ads-adpicture-content_type-object_id-INITIAL_FORMS':0}
        resp = self.c.post(reverse('add'), ad_home)
        self.assertEqual(resp['Location'], 'http://www.achetersanscom.com/annonce/1/edit')
        # is mail sent to the user and the moderator
        self.assertEqual(len(mail.outbox), 2)
        resp = self.c.get('/annonce/1/edit')
        # is right home in form
        self.assertTrue('home' in resp.context)
        home = resp.context['home']
        # approve add
        home.moderated_object.approve()
        # check if mail is sent to the user when add approved
        self.assertEqual(len(mail.outbox), 3)
        # test changes
        ad_home['price'] = 724000
        resp = self.c.post(reverse('add'), ad_home)
        self.assertEqual(len(mail.outbox), 5)

class DeleteAdTestCase(TestCase):

    def setUp(self):
        self.c = Client(SERVER_NAME="www.achetersanscom.com")

    def test_delete_page(self):
        pass


class UserSignup(TestCase):

    def setUp(self):
        self.c = Client(SERVER_NAME="www.achetersanscom.com")

    def test_signup_and_activation_mail(self):
        # this to ensure authorisations for user creation
        call_command('check_permissions')
        resp = self.c.post(reverse('userena_signup'), {'email':'trou@ducul.com', 'password1':'password', 'password2':'password'})
        # 2 because we trace signup ...
        self.assertEqual(len(mail.outbox), 2)        
        #print mail.outbox[0].body
        urls = re.findall('http[s]?://www.achetersanscom.com(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', mail.outbox[0].body)
        #print urls[0]
        resp = self.c.get(urls[0])
        self.assertEqual(resp.status_code, 302)
        print resp['Location']
        #print resp






