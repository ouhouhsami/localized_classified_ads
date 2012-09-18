from geoads.forms import BaseAdForm
from moderation.forms import BaseModeratedObjectForm


class BaseModeratedAdForm(BaseModeratedObjectForm, BaseAdForm):
    pass