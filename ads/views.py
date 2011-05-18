# coding=utf-8
from datetime import datetime

from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.http import QueryDict
from django.contrib.gis.geos import Point, Polygon, GEOSGeometry
from django import forms
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.contrib import messages
from django.shortcuts import redirect
from django.forms.models import inlineformset_factory
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.contrib.contenttypes.models import ContentType
from django.contrib.gis.geos import fromstr

import floppyforms 
import django_filters
from django_filters.filters import Filter
from form_utils.forms import BetterForm
from profiles.models import UserProfile

from models import *
from forms import AdContactForm, HomeForSaleAdForm, HomeForSaleAdFilterSetForm
from widgets import PolygonWidget, CustomPointWidget
from filters import LocationFilter
from filtersets import HomeForSaleAdFilterSet


def search(request, search_id=None):
    """Search view
    
    """
    # must test if location is set in request.POST or in saved search ?
    # no, it doesn't work
    if search_id is None:
        filter = HomeForSaleAdFilterSet(request.POST or None)
        #value =  filter.form['location'].value()
        #print isinstance(value, basestring)
        #print filter.form
    else:
        home_for_sale = HomeForSaleSearch.objects.get(id = search_id)
        q = QueryDict(home_for_sale.search)
        filter = HomeForSaleAdFilterSet(q or None)
        if home_for_sale.user_profile.user != request.user:
            return Http404
    if request.POST.__contains__('save_and_search') and search_id is None:
        datas = request.POST.copy()
        del datas['save_and_search']
        del datas['csrfmiddlewaretoken']
        search =  datas.urlencode()
        user_profile = UserProfile.objects.get(user = request.user)
        home_for_sale_search = HomeForSaleSearch(search = search, 
                                                 user_profile = user_profile)
        home_for_sale_search.save()
        messages.add_message(request, messages.INFO, 
                             'Votre recherche a bien été sauvegardée.')
    return render_to_response('ads/search.html', {'filter': filter}, 
                              context_instance = RequestContext(request))

@login_required
def delete_search(request, search_id):
    """Delete search view

    """
    search = HomeForSaleSearch.objects.get(id = search_id)
    if search.user_profile.user.username == request.user.username:
        search.delete()
        messages.add_message(request, messages.INFO, 
                             'Votre recherche a bien été supprimée.')
        return redirect('userena_profile_detail', username=request.user.username)
    else:
        return Http404

@login_required
def add(request):
    form = HomeForSaleAdForm()
    #PictureFormset = inlineformset_factory(HomeForSaleAd, HomeForSaleAdPicture, extra=4, max_num=4, form=HomeForSaleAdPictureForm)
    PictureFormset = inlineformset_factory(HomeForSaleAd, HomeForSaleAdPicture, extra=4, max_num=4)
    picture_formset = PictureFormset()
    if request.method == 'POST':
        form = HomeForSaleAdForm(request.POST)
        if form.is_valid():
            instance = form.save(commit = False)
            instance.user_profile = UserProfile.objects.get(user = request.user)
            instance.save()
            print instance.location
            PictureFormset = inlineformset_factory(HomeForSaleAd, HomeForSaleAdPicture, extra=4, max_num=4)
            picture_formset = PictureFormset(request.POST, request.FILES, instance = instance)
            if picture_formset.is_valid():
                picture_formset.save()
            messages.add_message(request, messages.INFO, 'Votre annonce a bien été enregistrée, elle va être modérée, vous serez tenu informé de sa mise en ligne.')
            return HttpResponseRedirect(reverse('edit', args=[instance.id]))
    return render_to_response('ads/edit.html', {'form':form, 'picture_formset':picture_formset}, context_instance = RequestContext(request))

def view(request, ad_id):
    ad = HomeForSaleAd.objects.get(id = ad_id)
    map_widget = CustomPointWidget(ads = [ad], id = "location", controls = False)
    
    if ad.delete_date is not None:
        return Http404
    contact_form = AdContactForm()
    if request.method == 'POST':
        contact_form = AdContactForm(request.POST)
        if contact_form.is_valid():
            instance = contact_form.save(commit = False)
            instance.content_object = ad
            page_user = get_object_or_404(User, username=request.user.username)
            profile_class = get_profile_model()
            profile = get_object_or_404(profile_class, user = page_user)
            instance.user_profile = profile
            instance.save()
            send_mail('Demande d\'information concernant votre annonce', instance.message, instance.user_profile.user.email, [ad.user_profile.user.email], fail_silently=False)
            messages.add_message(request, messages.INFO, 'Votre message a bien été envoyé au vendeur du bien.')
    return render_to_response('ads/view.html', {'ad':ad, 'contact_form':contact_form, 'map_widget':map_widget.render('name', '', {})}, context_instance = RequestContext(request))

@login_required
def edit(request, ad_id):
    h = HomeForSaleAd.unmoderated_objects.get(id = ad_id)
    PictureFormset = inlineformset_factory(HomeForSaleAd, HomeForSaleAdPicture, extra=4, max_num=4)
    picture_formset = PictureFormset(instance = h)
    if h.user_profile.user.username == request.user.username:
        form = HomeForSaleAdForm(instance = h)
        if request.method == 'POST':
            form = HomeForSaleAdForm(request.POST, instance = h)
            if form.is_valid():
                instance = form.save(commit = False)
                instance.save()
                PictureFormset = inlineformset_factory(HomeForSaleAd, HomeForSaleAdPicture, extra=4, max_num=4)
                picture_formset = PictureFormset(request.POST, request.FILES, instance=instance)
                if picture_formset.is_valid():
                    picture_formset.save()
                
                messages.add_message(request, messages.INFO, 'Votre annonce a bien été modifiée, elle va être modérée, vous serez tenu informé de sa mise en ligne.')
        return render_to_response('ads/edit.html', {'form':form, 'picture_formset':picture_formset}, context_instance = RequestContext(request))
    else:
        return Http404

@login_required
def delete(request, ad_id):
    h = HomeForSaleAd.objects.get(id = ad_id)
    if request.user == h.user_profile.user:
        h.delete_date = datetime.now()
        h.save()
        messages.add_message(request, messages.INFO, 'Votre annonce a bien été supprimée.')
        return redirect('profile_detail', username=request.user.username)
    else:
        return Http404