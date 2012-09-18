# Create your views here.
from geoads.views import AdUpdateView
from django.http import Http404


class ModeratedAdUpdateView(AdUpdateView):
    """
    Class base update moderated ad

    """
    def get_object(self, queryset=None):
        """ Hook to ensure object is owned by request.user. """
        # we shoud inherit from method get_object of parent class ...
        obj = self.model.unmoderated_objects.get(id=self.kwargs['pk'])

        if not obj.user == self.request.user:
            raise Http404
        # TODO: ugly hack don't understand, if not line below, value is converted
        obj.location = str(obj.location)
        return obj
