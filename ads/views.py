# coding=utf-8
"""
Views for ads application

This module provides CRUD absraction functions.
"""

from datetime import datetime

from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.template import RequestContext
from django.http import HttpResponseRedirect, QueryDict
from django.contrib.gis.geos import Point, Polygon, GEOSGeometry
from django import forms
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.contrib import messages
from django.shortcuts import redirect
from django.forms.models import inlineformset_factory
from django.contrib.contenttypes.generic import generic_inlineformset_factory
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.contrib.contenttypes.models import ContentType
from django.contrib.gis.geos import fromstr
from django.contrib.sites.models import Site
from django.core import serializers
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.template.loader import render_to_string
from django.contrib.gis.utils import GeoIP
from django.utils.translation import ugettext as _

import floppyforms
import django_filters
from django_filters.filters import Filter
from form_utils.forms import BetterForm

from pygeocoder import Geocoder, GeocoderError
from django.contrib.gis.gdal import SpatialReference, CoordTransform
from django.contrib.gis.geos import Point

from ads.models import AdSearch, AdPicture
from ads.forms import AdPictureForm, AdContactForm
from ads.widgets import PolygonWidget, CustomPointWidget
from ads.filters import LocationFilter
from ads.decorators import site_decorator

# to localize client
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

@site_decorator
def search(request, search_id=None, Ad=None, AdForm=None, AdFilterSet=None):
    """Search view
    
    """
    if request.method != 'POST' and request.GET == {} and search_id is None:
        search = False
        filter = AdFilterSet(None, search=search)
        # center map
        g = GeoIP()
        ip = get_client_ip(request)
        # for testing purpose 
        if ip == '127.0.0.1':
            ip = '129.102.64.54'
        latlon = g.lat_lon(ip)
        initial_ads = Ad.objects.select_related()\
                            .filter(delete_date__isnull=True)\
                            .filter(_relation_object__moderation_status = 1)\
                            .order_by('-create_date')[0:10]
        return render_to_response('ads/search.html', 
                                  {'filter': filter, 'search':search, 
                                   'initial_ads':initial_ads}, 
                                  context_instance = RequestContext(request))
    else:
        search = True
        if search_id is not None:
            ad_search = AdSearch.objects.get(id = search_id)
            q = QueryDict(ad_search.search)
            filter = AdFilterSet(q or None, search = search)
            if ad_search.user_profile.user != request.user:
                raise Http404
        else:
            filter = AdFilterSet(request.POST or None, search = search)
        if request.POST.__contains__('save_and_search') and search_id is None:
            datas = request.POST.copy()
            del datas['save_and_search']
            del datas['csrfmiddlewaretoken']
            search =  datas.urlencode()
            user_profile = request.user.get_profile()
            ad_search = AdSearch(search = search,
                         content_type = ContentType.objects.get_for_model(Ad), 
                         user_profile = user_profile)
            ad_search.save()
            userena_profile_detail_url = reverse('userena_profile_detail', 
                                             args=[user_profile.user.username])
            messages.add_message(request, messages.INFO,
            _(u'Votre recherche a bien été sauvegardée '+
              u'dans <a href="%s">votre compte</a>.') 
            % (userena_profile_detail_url))
        # len method is speeder than count()
        nb_of_results = len(filter.qs)
        if nb_of_results == 0:
            messages.add_message(request, messages.INFO, 
            _(u'Aucune annonce ne correspond à votre recherche. '+
              u'Elargissez votre zone de recherche ou modifiez les critères.'))
        if nb_of_results >= 1:
            ann = _(u'annonces')
            if nb_of_results == 1:
                ann = _(u'annonce')
            if request.user.is_authenticated():
                messages.add_message(request, messages.INFO, 
                             _(u'%s %s correspondant à votre recherche') % 
                              (nb_of_results, ann))
            else:
                sign_url = reverse('userena_signup', args=[])
                messages.add_message(request, messages.INFO, 
                      _(u'%s %s correspondant à votre recherche. '+ 
                        u'<a href="%s">Inscrivez-vous</a> pour recevoir'+ 
                        u' les alertes mail ou enregistrer votre recherche.') \
                           % (nb_of_results, ann, sign_url))
        return render_to_response('ads/search.html', {'filter': filter,
                                                      'search':search}, 
                                    context_instance = RequestContext(request))

@login_required
def delete_search(request, search_id):
    """Delete search view

    """
    search = AdSearch.objects.get(id = search_id)
    if search.user_profile.user.username == request.user.username:
        search.delete()
        messages.add_message(request, messages.INFO, 
                             _(u'Votre recherche a bien été supprimée.'))
        return redirect('userena_profile_detail', 
                        username=request.user.username)
    else:
        raise Http404

@site_decorator
def view(request, ad_slug, Ad=None, AdForm=None, AdFilterSet=None):
    try:
        ad = Ad.objects.get(slug = ad_slug)
    except Ad.DoesNotExist:
        raise Http404
    sent_mail = False
    if ad.delete_date is not None or ad.moderated_object.moderation_status != 1:
        raise Http404
    contact_form = AdContactForm()
    if request.method == 'POST':
        contact_form = AdContactForm(request.POST)
        if contact_form.is_valid():
            instance = contact_form.save(commit = False)
            instance.content_object = ad
            instance.user_profile = request.user.get_profile()
            instance.save()
            send_mail(_(u'[%s] Demande d\'information concernant votre annonce') \
            % (Site.objects.get_current().name), 
               instance.message, 
               instance.user_profile.user.email, 
               [ad.user_profile.user.email], 
               fail_silently=False)
            sent_mail = True
            messages.add_message(request, messages.INFO, 
                                 _(u'Votre message a bien été envoyé.'))
    if request.is_ajax():
        return render_to_response('ads/view_ajax.html', {'ad':ad, 
                                  'contact_form':contact_form}, 
                                  context_instance = RequestContext(request))
    else:
        return render_to_response('ads/view.html', {'ad':ad, 
                                  'contact_form':contact_form, 
                                  'sent_mail':sent_mail}, 
                                  context_instance = RequestContext(request))


@site_decorator
@login_required(login_url='/accounts/signup/')
def add(request, Ad=None, AdForm=None, AdFilterSet=None):
    form = AdForm()
    PictureFormset = generic_inlineformset_factory(AdPicture, 
                                                   extra=4, max_num=4)
    picture_formset = PictureFormset()
    if request.method == 'POST':
        form = AdForm(request.POST)
        if form.is_valid():
            instance = form.save(commit = False)
            instance.user_profile = request.user.get_profile()
            # line below due to the fact that location and address 
            # are excluded from adform
            print form.cleaned_data['user_entered_address']
            instance.location = form.cleaned_data['location']
            instance.address = form.cleaned_data['address']
            # add location and address fields
            # if one day we need to change projection
            # origin_coord = SpatialReference(900913)
            # target_coord = SpatialReference(4326)
            # trans = CoordTransform(origin_coord, target_coord)
            instance.save()
            PictureFormset = generic_inlineformset_factory(AdPicture, 
                                                           extra=4, max_num=4)
            picture_formset = PictureFormset(request.POST, request.FILES, 
                                             instance = instance)
            if picture_formset.is_valid():
                picture_formset.save()
            # here we need to add changed_by to moderated object 
            # to get email notification
            instance.moderated_object.changed_by = request.user
            instance.moderated_object.save()
            message = render_to_string('ads/emails/ad_create_email_message.txt')
            subject = render_to_string('ads/emails/ad_create_email_subject.txt', 
                                  {'site_name':Site.objects.get_current().name})
            send_mail(subject, message, 'contact@achetersanscom.com', 
                      [instance.user_profile.user.email], fail_silently=True)
            return redirect('completed', permanent=True)
        send_mail(_(u"[%s] %s valide l'ajout d'un bien") % 
                  (Site.objects.get_current().name, request.user.email), 
                  "%s" % (form.errors), 'contact@achetersanscom.com', 
                  ["contact@achetersanscom.com"], fail_silently=True)
    else:
        send_mail(_(u"[%s] %s est sur la page d'ajout d'un bien") % 
                  (Site.objects.get_current().name, request.user.email), "", 
                  'contact@achetersanscom.com', 
                  ["contact@achetersanscom.com"], fail_silently=True)
    return render_to_response('ads/edit.html', {'form':form, 
                              'picture_formset':picture_formset}, 
                              context_instance = RequestContext(request))


@site_decorator
@login_required
def edit(request, ad_id, Ad=None, AdForm=None, AdFilterSet=None):
    h = Ad.unmoderated_objects.get(id = ad_id)
    # hack de merde, je ne comprends pas, sinon il convertit la valeur
    h.location = str(h.location)
    # h = Ad.objects.get(id = ad_id)
    PictureFormset = generic_inlineformset_factory(AdPicture, 
                                        form=AdPictureForm, extra=4, max_num=4)
    picture_formset = PictureFormset(instance = h)
    if h.user_profile.user.username == request.user.username:
        #form = AdForm(h.__dict__)
        form = AdForm(h.moderated_object.changed_object.__dict__)
        if request.method == 'POST':
            form = AdForm(request.POST, instance = h)
            #print 'je suis la'
            if form.is_valid():
                #print 'mais pas la'
                instance = form.save(commit = False)
                # line below due to the fact that location and address 
                # are excluded from adform
                instance.location = form.cleaned_data['location']
                instance.address = form.cleaned_data['address']                
                instance.save()
                PictureFormset = generic_inlineformset_factory(AdPicture, 
                                        form=AdPictureForm, extra=4, max_num=4)
                picture_formset = PictureFormset(request.POST, request.FILES, 
                                                 instance=instance)
                if picture_formset.is_valid():
                    picture_formset.save()
                # here we DONT need to add changed_by to moderated object 
                # to get email notification because moderated object already 
                # know about user from 'add' function
                # below, to be sure that images are displayed
                picture_formset = PictureFormset(instance = h)
                message = render_to_string(
                                  'ads/emails/ad_update_email_message.txt', {})
                subject = render_to_string(
                                  'ads/emails/ad_update_email_subject.txt', 
                                 {'site_name':Site.objects.get_current().name})
                send_mail(subject, message, 'contact@achetersanscom.com', 
                          [instance.user_profile.user.email], 
                          fail_silently=True)
                return redirect('completed', permanent=True)
                # below to force real value of fields
                h = Ad.unmoderated_objects.get(id = ad_id)
                form = AdForm(h.moderated_object.changed_object.__dict__)
            # if error, here, we return form
        return render_to_response('ads/edit.html', 
                                  {'form':form, 
                                   'picture_formset':picture_formset, 
                                   'home':h}, 
                                  context_instance = RequestContext(request))
    else:
        raise Http404

def completed(request):
    return render_to_response('ads/validation.html', {}, 
                               context_instance=RequestContext(request))

@site_decorator
@login_required
def delete(request, ad_id, Ad=None, AdForm=None, AdFilterSet=None):
    h = Ad.unmoderated_objects.get(id = ad_id)
    if request.user == h.user_profile.user:
        h.delete_date = datetime.now()
        h.save()
        serialized_obj = serializers.serialize('json', [ h, ])
        path = default_storage.save('deleted/%s-%s.json' % (h.id, h.slug), 
                                    ContentFile(serialized_obj))
        messages.add_message(request, messages.INFO, 
                             _(u'Votre annonce a bien été supprimée.'))
        h.delete()
        return redirect('userena_profile_detail', 
                        username=request.user.username)
    else:
        raise Http404