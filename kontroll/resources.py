from import_export import resources
from .models import Avvik, Customer


class AvvikResource(resources.ModelResource):
    class Meta:
        model = Avvik


class CustomerResource(resources.ModelResource):
    class Meta:
        model = Customer
