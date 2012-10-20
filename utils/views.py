from datetime import datetime

from django.http import Http404
from django.core.files.storage import default_storage
from django.core import serializers
from django.core.files.base import ContentFile
from django.http import HttpResponseRedirect

from geoads.views import AdUpdateView, AdDeleteView


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


class CustomAdDeleteView(AdDeleteView):
    """
    Custom Ad delete view that keep deleted items in json format
    """
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete_date = datetime.now()
        self.object.save()
        serialized_obj = serializers.serialize('json', [self.object, ])
        default_storage.save('deleted/%s-%s.json' % (self.object.id,
                                                    self.object.slug),
                                    ContentFile(serialized_obj))
        self.object.delete()
        return HttpResponseRedirect(self.get_success_url())
