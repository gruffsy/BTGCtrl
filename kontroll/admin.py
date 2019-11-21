from django.contrib import admin
from .models import Month, Customer, Extinguishant, Object, ObjTr
# Register your models here.

admin.site.register(Month),
admin.site.register(Customer),
admin.site.register(Extinguishant),
admin.site.register(Object),
admin.site.register(ObjTr),

