# coding=utf-8
import logging

from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.hashers import make_password
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import set_urlconf
from django.core import mail

from moderation.models import ModeratedObject

from django.core.urlresolvers import reverse
from sites.achetersanscom.ads.factories import UserFactory, HomeForSaleAdFactory, HomeForSaleAdSearchFactory
from sites.achetersanscom.ads.models import HomeForSaleAd

logger = logging.getLogger(__name__)


class AcheterSansComBaseTestCase(TestCase):
    '''
    Base Test Case to setUp easily TestCase,
    especially dealing with some obscures
    urlconf and settings.DEBUG
    '''
    def setUp(self):
        self.c = Client(SERVER_NAME="achetersanscom.dev", SERVER_PORT="8000")
        from sites.achetersanscom import urls
        set_urlconf(urls)
        from django.conf import settings
        settings.DEBUG = True


class HomeTestCase(AcheterSansComBaseTestCase):

    def test_home(self):
        # TIP: in TestCase, we need to add urlconf to the reverse function
        # so that reverse know where to look for name
        resp = self.c.get(reverse('search', 'sites.achetersanscom.urls'))
        self.assertEqual(resp.status_code, 200)

    def test_get_home_filter_not_logged(self):
        resp = self.c.get(reverse('search', 'sites.achetersanscom.urls'), {'foo': 'bar'})
        self.assertEqual(resp.status_code, 200)
        # we should test message

    def test_get_home_filter_logged(self):
        user = UserFactory.create(password="coolpwd")
        self.c.login(username=user.username, password='coolpwd')
        resp = self.c.get(reverse('search', 'sites.achetersanscom.urls'), {'foo': 'bar'})
        self.assertEqual(resp.status_code, 200)
        # we should test message

    def test_get_home_filter_not_logged_results(self):
        home = HomeForSaleAdFactory.create()
        resp = self.c.get(reverse('search', 'sites.achetersanscom.urls'), {'foo': 'bar'})
        self.assertEqual(resp.status_code, 200)
        home.delete()
        # we should test message

    def test_get_home_filter_logged_results(self):
        home = HomeForSaleAdFactory.create()
        user = UserFactory.create(password="coolpwd")
        self.c.login(username=user.username, password='coolpwd')
        resp = self.c.get(reverse('search', 'sites.achetersanscom.urls'), {'foo': 'bar'})
        self.assertEqual(resp.status_code, 200)
        home.delete()
        # we should test message

    #def tearDown(self):
    #    pass


class CreateHomeForSaleTestCase(AcheterSansComBaseTestCase):

    def test_get_create_homeforsalead_unlogged_user(self):
        resp = self.c.get(reverse('add', 'sites.achetersanscom.urls'))
        self.assertEqual(resp.status_code, 302)

    def test_get_create_homeforsalead_logged_user(self):
        user = UserFactory.create(password="coolpwd")
        self.c.login(username=user.username, password='coolpwd')
        resp = self.c.get(reverse('add', 'sites.achetersanscom.urls'))
        self.assertEqual(resp.status_code, 200)

    def test_post_create_homeforsalead_invalid_datas(self):
        user = UserFactory.create(password="coolpwd")
        self.c.login(username=user.username, password='coolpwd')
        resp = self.c.post(reverse('add', 'sites.achetersanscom.urls'))
        self.assertEqual(resp.status_code, 200)
        form = resp.context_data['form']
        self.assertFalse(form.is_valid())

    def test_post_create_homeforsalead_valid_datas(self):
        user = UserFactory.create(password="coolpwd")
        self.c.login(username=user.username, password='coolpwd')
        ad_home = {'user_profile': user, 'price': 624000,
                   'habitation_type': "0", 'surface': 63, 'nb_of_rooms': 3,
                   'user_entered_address': "5 rue de Verneuil, Paris",
                   'nb_of_bedrooms': 2,
                   'geoads-adpicture-content_type-object_id-TOTAL_FORMS': 1,
                   'geoads-adpicture-content_type-object_id-INITIAL_FORMS': 0}
        resp = self.c.post(reverse('add', 'sites.achetersanscom.urls'), ad_home)
        self.assertEqual(resp.status_code, 301)
        self.c.login(username=user.username, password='coolpwd')
        # bad surface
        ad_home = {'user_profile': user, 'price': 624000,
                   'habitation_type': "0", 'surface': 'a', 'nb_of_rooms': 3,
                   'user_entered_address': "5 rue de Verneuil, Paris",
                   'nb_of_bedrooms': 2,
                   'geoads-adpicture-content_type-object_id-TOTAL_FORMS': 1,
                   'geoads-adpicture-content_type-object_id-INITIAL_FORMS': 0}
        resp = self.c.post(reverse('add', 'sites.achetersanscom.urls'), ad_home)
        self.assertEqual(resp.status_code, 200)
        #print resp.context_data['form']['surface'].errors
        self.assertEquals(resp.context_data['form']['surface'].errors, [u"Entrez une surface en mètres carré."])
        #below same test, but doesn't works: seems like form doesn't have a surface field ! why ?
        #self.assertFormError(resp, 'form', 'surface', u"Entrez une surface en mètres carré.")
        # test if ad has been created
        self.assertEquals(HomeForSaleAd.unmoderated_objects.filter(user=user).count(), 1)
        # test if ad is not available
        self.assertEquals(HomeForSaleAd.objects.filter(user=user).count(), 0)
        # approve
        ModeratedObject.objects.all()[0].approve()
        # test if ad is now available
        self.assertEquals(HomeForSaleAd.objects.filter(user=user).count(), 1)

    def test_post_update_homeforsale(self):
        home = HomeForSaleAdFactory.create()
        user = home.user
        user.password = make_password('bla')
        user.save()
        self.c.login(username=user.username, password='bla')
        resp = self.c.post(reverse('edit', 'sites.achetersanscom.urls', kwargs={'pk': home.id}))
        self.assertEqual(resp.status_code, 200)

    def test_get_update_homeforsale(self):
        # test for user that doesn't own the ad => throw 404
        home = HomeForSaleAdFactory.create()
        user = UserFactory.create(password="coolpwd")
        self.c.login(username=user.username, password='coolpwd')
        resp = self.c.get(reverse('edit', 'sites.achetersanscom.urls', kwargs={'pk': home.id}))
        self.assertEqual(resp.status_code, 404)

    #def tearDown(self):
    #    pass


class SignalTestCase(AcheterSansComBaseTestCase):

    def test_create_home(self):
        # see if moderation works fine
        home = HomeForSaleAdFactory.create(price="20")
        self.assertEquals(HomeForSaleAd.objects.all().count(), 0)
        self.assertEquals(ModeratedObject.objects.all().count(), 1)
        home.moderated_object.approve()
        self.assertEquals(HomeForSaleAd.objects.all().count(), 1)
        self.assertEquals(ModeratedObject.objects.all().count(), 1)
        self.assertEquals(len(mail.outbox), 3)
        home.delete()

    def test_create_search(self):
        logger.info('HomeForSaleAdSearch create')
        search = 'separate_dining_room=1&energy_consumption=&terrace=1&parking=&separate_toilet=1&doorman=1&balcony=1&nb_of_rooms_1=&nb_of_rooms_0=&bathroom=1&duplex=1&floor_0=&elevator=1&surface_1=&location=&top_floor=1&nb_of_bedrooms_1=&nb_of_bedrooms_0=&surface_0=&not_overlooked=1&cellar=1&separate_entrance=1&digicode=1&intercom=1&search=search&air_conditioning=1&fireplace=&floor_1=&kitchen=1&price_1=&price_0=&ground_floor=1&alarm=1&heating=&shower=1&swimming_pool=1&emission_of_greenhouse_gases='
        home_search = HomeForSaleAdSearchFactory.create(search=search,
            content_type=ContentType.objects.get_for_model(HomeForSaleAd))
        #print 'len', len(mail.outbox)
        #print homeforsalead_search.content_type
        #print ContentType.objects.get_for_model(HomeForSaleAd)
        #print HomeForSaleAd.objects.all()
        logger.info('HomeForSaleAd create')
        home = HomeForSaleAdFactory.create(price="21")
        #nb_of_mails = len(mail.outbox)
        #ModeratedObject.objects.all()[0].approve()
        logger.info('HomeForSaleAd is moderated')
        home.moderated_object.approve()
        #print '>>>>>>>>>>>>', len(mail.outbox) - nb_of_mails
        #print 'len', len(mail.outbox)
        #for m in mail.outbox:
        #    print m.subject
        home_search.public = True
        logger.info("HomeForSaleAdSearch is now public, we should send some mails to vendors for potential buyers")
        home_search.save()
        #print '>>>>>>>>>>>>', len(mail.outbox) - nb_of_mails
        #print 'len', len(mail.outbox)
        #for m in mail.outbox:
        #    print m.subject
        home_search.delete()
        home.delete()

'''
class StaticPageTestCase(AcheterSansComBaseTestCase):

    def test_header(self):
        # test if header of static page is set to the current sites
        resp = self.c.get('/a-propos/')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'site_title.html')
        print resp.templates
        for t in resp.templates:
            print t.name
        from django.template.loader import render_to_string
        rendered = render_to_string('site_title.html')
        print rendered
'''
