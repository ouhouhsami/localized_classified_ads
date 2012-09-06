# coding=utf-8
from django.utils.translation import ugettext as _

from geoads.views import AdSearchView

from sites.achetersanscom.ads.models import HomeForSaleAd
from sites.achetersanscom.ads.filtersets import HomeForSaleAdFilterSet


SUPP_MSG = _(u'<br/> <a class="btn btn-primary">Inscrivez-vous</a> pour \
            créer une alerte email ou déposer une annonce de recherche \
            et être contacté directement par les propriétaires.')


class HomeForSaleAdSearchView(AdSearchView):
    model = HomeForSaleAd
    filterset_class = HomeForSaleAdFilterSet

    def get_no_results_msg(self):
        msg = super(HomeForSaleAdSearchView, self).get_no_results_msg()
        if not self.request.user.is_authenticated():
            return msg + SUPP_MSG
        return msg

    def get_results_msg(self):
        msg = super(HomeForSaleAdSearchView, self).get_results_msg()
        if not self.request.user.is_authenticated():
            return msg + SUPP_MSG
        return msg
