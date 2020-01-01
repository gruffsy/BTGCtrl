from import_export import resources
from .models import Avvik


class AvvikResource(resources.ModelResource):
    class Meta:
        model = Avvik
