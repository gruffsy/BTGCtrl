from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Month, Customer, Slokketype, Extinguishant, Object, ObjTr, Avvik


class AvvikAdmin(ImportExportModelAdmin):
    pass


class CustomerAdmin(ImportExportModelAdmin):
    pass

# Register your models here.

admin.site.register(Month),
admin.site.register(Customer, CustomerAdmin),
admin.site.register(Slokketype),
admin.site.register(Extinguishant),
admin.site.register(Object),
admin.site.register(ObjTr),
admin.site.register(Avvik, AvvikAdmin),
