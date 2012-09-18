# coding=utf-8
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse_lazy

from geoads.views import AdSearchView

from sites.louersanscom.ads.models import HomeForRentAd


SUPP_MSG = _(u'<br/> <a class="btn btn-primary">Inscrivez-vous</a> pour \
            créer une alerte email ou déposer une demande de location \
            et être contacté directement par les propriétaires.' % reverse_lazy('userena_signup'))


class HomeForRentAdSearchView(AdSearchView):
    model = HomeForRentAd

    def get_no_results_msg(self):
        msg = super(HomeForRentAdSearchView, self).get_no_results_msg()
        if not self.request.user.is_authenticated():
            return msg + SUPP_MSG
        return msg

    def get_results_msg(self):
        msg = super(HomeForRentAdSearchView, self).get_results_msg()
        if not self.request.user.is_authenticated():
            return msg + SUPP_MSG
        return msg
