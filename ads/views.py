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
from django.contrib.contenttypes.generic import generic_inlineformset_factory
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.contrib.contenttypes.models import ContentType
from django.contrib.gis.geos import fromstr


import floppyforms
import django_filters
from django_filters.filters import Filter
from form_utils.forms import BetterForm
from profiles.models import UserProfile

from models import HomeForSaleAd, AdSearch, AdPicture
from forms import AdContactForm, HomeForSaleAdForm, HomeForSaleAdFilterSetForm
from widgets import PolygonWidget, CustomPointWidget
from filters import LocationFilter
from filtersets import HomeForSaleAdFilterSet
from decorators import site_decorator

@site_decorator
def search(request, search_id=None, Ad=None, AdForm=None, AdFilterSet=None):
    """Search view
    
    """
    total_ads = Ad.objects.all().count()
    if request.method != 'POST' and request.GET == {} and search_id is None:
        search = False
        filter = AdFilterSet(None, search = search)
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
            user_profile = UserProfile.objects.get(user = request.user)
            ad_search = AdSearch(search = search,content_type = ContentType.objects.get_for_model(Ad), 
                                                 user_profile = user_profile)
            ad_search.save()
            messages.add_message(request, messages.INFO,
                             'Votre recherche a bien été sauvegardée.')
        nb_of_results = filter.qs.count()
        if nb_of_results == 0:
            messages.add_message(request, messages.INFO, 
                             'Aucune annonce ne correspond à votre recherche')
        if nb_of_results == 1:
            messages.add_message(request, messages.INFO, 
                             '1 annonce correspondant à votre recherche')
        if nb_of_results > 1:
            if request.user.is_authenticated():
                messages.add_message(request, messages.INFO, 
                             '%s annonces correspondant à votre recherche' % (filter.qs.count()))
            else:
                sign_url = reverse('userena_signup', args=[])
                messages.add_message(request, messages.INFO, 
                             '%s annonces correspondant à votre recherche. <a href="%s">Inscrivez-vous</a> pour recevoir les alertes mail !' % (filter.qs.count(), sign_url))
    return render_to_response('ads/search.html', {'filter': filter, 'search':search, 'total_ads':total_ads}, 
                              context_instance = RequestContext(request))

@login_required
def delete_search(request, search_id):
    """Delete search view

    """
    search = AdSearch.objects.get(id = search_id)
    if search.user_profile.user.username == request.user.username:
        search.delete()
        messages.add_message(request, messages.INFO, 
                             'Votre recherche a bien été supprimée.')
        return redirect('userena_profile_detail', username=request.user.username)
    else:
        raise Http404

@site_decorator
def view(request, ad_id, Ad=None, AdForm=None, AdFilterSet=None):
    ad = Ad.objects.get(id = ad_id)
    map_widget = CustomPointWidget(ads = [ad], id = "location", controls = False)
    
    if ad.delete_date is not None or ad.moderated_object.moderation_status != 1:
        raise Http404
    contact_form = AdContactForm()
    if request.method == 'POST':
        contact_form = AdContactForm(request.POST)
        if contact_form.is_valid():
            instance = contact_form.save(commit = False)
            instance.content_object = ad
            instance.user_profile = UserProfile.objects.get(user = request.user)
            instance.save()
            send_mail('[AcheterSansCom.com] Demande d\'information concernant votre annonce', instance.message, instance.user_profile.user.email, [ad.user_profile.user.email], fail_silently=False)
            messages.add_message(request, messages.INFO, 'Votre message a bien été envoyé au vendeur du bien.')
    if request.is_ajax():
        return render_to_response('ads/view_ajax.html', {'ad':ad, 'contact_form':contact_form, 'map_widget':map_widget.render('name', '', {})}, context_instance = RequestContext(request))
    else:
        return render_to_response('ads/view.html', {'ad':ad, 'contact_form':contact_form, 'map_widget':map_widget.render('name', '', {})}, context_instance = RequestContext(request))


@site_decorator
@login_required
def add(request, Ad=None, AdForm=None, AdFilterSet=None):
    form = AdForm()
    PictureFormset = generic_inlineformset_factory(AdPicture, extra=4, max_num=4)
    picture_formset = PictureFormset()
    if request.method == 'POST':
        form = AdForm(request.POST)
        if form.is_valid():
            instance = form.save(commit = False)
            instance.user_profile = UserProfile.objects.get(user = request.user)
            instance.save()
            PictureFormset = generic_inlineformset_factory(AdPicture, extra=4, max_num=4)
            picture_formset = PictureFormset(request.POST, request.FILES, instance = instance)
            if picture_formset.is_valid():
                picture_formset.save()
            messages.add_message(request, messages.INFO, 'Votre annonce a bien été enregistrée, elle va être modérée, vous serez tenu informé de sa mise en ligne.')
            return HttpResponseRedirect(reverse('edit', args=[instance.id]))
    return render_to_response('ads/edit.html', {'form':form, 'picture_formset':picture_formset}, context_instance = RequestContext(request))


@site_decorator
@login_required
def edit(request, ad_id, Ad=None, AdForm=None, AdFilterSet=None):
    h = Ad.unmoderated_objects.get(id = ad_id)
    PictureFormset = generic_inlineformset_factory(AdPicture, extra=4, max_num=4)
    picture_formset = PictureFormset(instance = h)
    if h.user_profile.user.username == request.user.username:
        form = AdForm(h.__dict__)
        if request.method == 'POST':
            form = AdForm(request.POST, instance = h)
            if form.is_valid():
                instance = form.save(commit = False)
                instance.save()
                PictureFormset = generic_inlineformset_factory(AdPicture, extra=4, max_num=4)
                picture_formset = PictureFormset(request.POST, request.FILES, instance=instance)
                if picture_formset.is_valid():
                    picture_formset.save()
                messages.add_message(request, messages.INFO, 'Votre annonce a bien été modifiée, elle va être modérée, vous serez tenu informé de sa mise en ligne.')
        return render_to_response('ads/edit.html', {'form':form, 'picture_formset':picture_formset, 'home':h}, context_instance = RequestContext(request))
    else:
        raise Http404

@site_decorator
@login_required
def delete(request, ad_id, Ad=None, AdForm=None, AdFilterSet=None):
    h = Ad.objects.get(id = ad_id)
    if request.user == h.user_profile.user:
        h.delete_date = datetime.now()
        h.save()
        messages.add_message(request, messages.INFO, 'Votre annonce a bien été supprimée.')
        return redirect('profile_detail', username=request.user.username)
    else:
        raise Http404