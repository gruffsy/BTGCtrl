from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Month, Customer, Slokketype, Extinguishant, Object, ObjTr, Avvik


@admin.register(Avvik)
class AvvikAdmin(ImportExportModelAdmin):
    pass


# Register your models here.

admin.site.register(Month),
admin.site.register(Customer),
admin.site.register(Slokketype),
admin.site.register(Extinguishant),
admin.site.register(Object),
admin.site.register(ObjTr),
