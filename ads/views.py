# coding=utf-8
"""
Views for ads application

This module provides CRUD absraction functions.
"""

from datetime import datetime

from django.contrib import messages
from django.contrib.contenttypes.generic import generic_inlineformset_factory
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.contrib.gis.utils import GeoIP
from django.core.urlresolvers import reverse
from django.core.mail import send_mail
from django.core import serializers
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.http import QueryDict, Http404, HttpResponseRedirect
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.template.loader import render_to_string
from django.utils.translation import ugettext as _
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.utils.decorators import method_decorator

from ads.models import Ad, AdSearch, AdPicture
from ads.forms import AdPictureForm, AdContactForm
from ads.decorators import site_decorator


class LoginRequiredMixin(object):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)


def get_client_ip(request):
    """
    Get client IP, used to localize client
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

'''
@site_decorator
def search(request, search_id=None, Ad=None, AdForm=None, AdFilterSet=None, **kwargs):
    """
    Search view
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
        # len method is speeder than count() !
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

'''

class AdSearchView(ListView):
    """
    Class based ad search view
    """
    model = Ad
    filterset_class = None
    search_id = None
    template_name = 'ads/search.html'

class AdSearchDeleteView(DeleteView):
    """
    Class based delete search ad
    """
    model = AdSearch
    
    def get_object(self, queryset=None):
        """ Ensure object is owned by request.user. """
        obj = super(AdSearchDeleteView, self).get_object()
        if not obj.user_profile.user == self.request.user:
            raise Http404
        return obj

    def get_success_url(self):
        """ Redirect to user account page"""
        messages.add_message(self.request, messages.INFO, 
                             _(u'Votre recherche a bien été supprimée.'))
        return reverse('userena_profile_detail', args=[self.request.user.username])

class AdDetailView(DetailView):
    """
    Class based detail ad
    """
    model = Ad # changed in urls
    context_object_name = 'ad'
    template_name = 'ads/view.html'

    def get_context_data(self, **kwargs):
        context = super(AdDetailView, self).get_context_data(**kwargs)
        context['contact_form'] = AdContactForm()
        context['sent_mail'] = False
        return context

    def post(self, request, *args, **kwargs):
        """ used for contact message between users """
        contact_form = AdContactForm(request.POST)
        if contact_form.is_valid():
            instance = contact_form.save(commit = False)
            instance.content_object = self.get_object()
            instance.user_profile = request.user.get_profile()
            instance.save()
            send_mail(_(u'[%s] Demande d\'information concernant votre annonce') \
            % (Site.objects.get_current().name), 
               instance.message, 
               instance.user_profile.user.email, 
               [self.get_object().user_profile.user.email], 
               fail_silently=False)
            sent_mail = True
            messages.add_message(request, messages.INFO, 
                                 _(u'Votre message a bien été envoyé.'))

        return render_to_response(self.template_name, {'ad':self.get_object(), 
                                  'contact_form':contact_form, 
                                  'sent_mail':sent_mail}, 
                                  context_instance = RequestContext(request))


class AdCreateView(LoginRequiredMixin, CreateView):
    """
    Class based create ad
    """
    model = Ad # overriden in specific project urls
    template_name = 'ads/edit.html'
    
    def form_valid(self, form):
        context = self.get_context_data()
        picture_formset = context['picture_formset']
        if picture_formset.is_valid():
            self.object = form.save(commit = False)
            self.object.user_profile = self.request.user.get_profile()
            self.object.location = form.cleaned_data['location']
            self.object.address = form.cleaned_data['address']
            self.object.save()
            picture_formset.instance = self.object
            picture_formset.save()
            self.object.moderated_object.changed_by = self.request.user
            self.object.moderated_object.save()
            message = render_to_string('ads/emails/ad_create_email_message.txt')
            subject = render_to_string('ads/emails/ad_create_email_subject.txt', 
                                  {'site_name':Site.objects.get_current().name})
            send_mail(subject, message, 'contact@achetersanscom.com', 
                      [instance.user_profile.user.email], fail_silently=True)
            return HttpResponseRedirect('complete/')
        send_mail(_(u"[%s] %s valide l'ajout d'un bien") % 
                  (Site.objects.get_current().name, self.request.user.email), 
                  "%s" % (form.errors), 'contact@achetersanscom.com', 
                  ["contact@achetersanscom.com"], fail_silently=True)
        #TODO: if formset not valid

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))
    
    def get_context_data(self, **kwargs):
        context = super(AdCreateView, self).get_context_data(**kwargs)
        if self.request.POST:
            PictureFormset = generic_inlineformset_factory(AdPicture, 
                                                   extra=4, max_num=4)
            context['picture_formset'] = PictureFormset(self.request.POST, 
                                                        self.request.FILES)
        else:
            PictureFormset = generic_inlineformset_factory(AdPicture, 
                                                   extra=4, max_num=4)
            context['picture_formset'] = PictureFormset()
        return context


class AdUpdateView(LoginRequiredMixin, UpdateView):
    """
    Class base update ad
    """
    model = Ad # overriden in specific project urls
    template_name = 'ads/edit.html'

    def form_valid(self, form):
        context = self.get_context_data()
        picture_formset = context['picture_formset']
        if picture_formset.is_valid():
            self.object = form.save(commit = False)
            self.object.location = form.cleaned_data['location']
            self.object.address = form.cleaned_data['address']
            self.object.save()
            picture_formset.instance = self.object
            picture_formset.save()
            message = render_to_string(
                              'ads/emails/ad_update_email_message.txt', {})
            subject = render_to_string(
                              'ads/emails/ad_update_email_subject.txt', 
                             {'site_name':Site.objects.get_current().name})
            send_mail(subject, message, 'contact@achetersanscom.com', 
                          [self.object.user_profile.user.email], 
                          fail_silently=True)
            return redirect('complete', permanent=True)
        #TODO: if formset not valid
        
    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

    def get_object(self, queryset=None):
        """ Hook to ensure object is owned by request.user. """
        obj = self.model.unmoderated_objects.get(id = self.kwargs['pk'])
        if not obj.user_profile.user == self.request.user:
            raise Http404
        # TODO: ugly hack don't understand, if not line below, value is converted
        obj.location = str(obj.location)
        return obj

    def get_context_data(self, **kwargs):
        context = super(AdUpdateView, self).get_context_data(**kwargs)
        if self.request.POST:
            PictureFormset = generic_inlineformset_factory(AdPicture, 
                                                   extra=4, max_num=4)
            context['picture_formset'] = PictureFormset(self.request.POST, 
                                                  self.request.FILES,
                                                  instance = context['object'])
        else:
            PictureFormset = generic_inlineformset_factory(AdPicture, 
                                                   extra=4, max_num=4)
            context['picture_formset'] = PictureFormset(instance = context['object'])
        return context


class CompleteView(LoginRequiredMixin, TemplateView):
    template_name = "ads/validation.html"

class AdDeleteView(LoginRequiredMixin, DeleteView):
    """
    Class based delete ad
    """
    model = Ad # "normally" overrided in specific project urls
    template_name = "ads/ad_confirm_delete.html"

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete_date = datetime.now()
        self.object.save()
        serialized_obj = serializers.serialize('json', [ self.object, ])
        path = default_storage.save('deleted/%s-%s.json' % (self.object.id, 
                                                          self.object.slug), 
                                    ContentFile(serialized_obj))
        self.object.delete()
        return HttpResponseRedirect(self.get_success_url())

    def get_queryset(self):
        return self.model.unmoderated_objects.all()

    def get_object(self, queryset=None):
        """ Ensure object is owned by request.user. """
        obj = super(AdDeleteView, self).get_object()
        if not obj.user_profile.user == self.request.user:
            raise Http404
        return obj

    def get_success_url(self):
        """ Redirect to user account page"""
        messages.add_message(self.request, messages.INFO, 
                             _(u'Votre annonce a bien été supprimée.'))
        return reverse('userena_profile_detail', args=[self.request.user.username])