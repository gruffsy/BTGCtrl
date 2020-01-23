from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Month, Customer, Slokketype, Extinguishant, Object, ObjTr, Avvik


class AvvikAdmin(ImportExportModelAdmin):
    pass

class CustomerAdmin(ImportExportModelAdmin):
    pass

class ExtinguishantAdmin(ImportExportModelAdmin):
    pass

class ObjectAdmin(ImportExportModelAdmin):
    pass

class SlokketypeAdmin(ImportExportModelAdmin):
    pass

class ObjTrAdmin(ImportExportModelAdmin):
    pass
# Register your models here.

admin.site.register(Month),
admin.site.register(Customer, CustomerAdmin),
admin.site.register(Slokketype, SlokketypeAdmin),
admin.site.register(Extinguishant, ExtinguishantAdmin),
admin.site.register(Object, ObjectAdmin),
admin.site.register(ObjTr, ObjTrAdmin),
admin.site.register(Avvik, AvvikAdmin),
