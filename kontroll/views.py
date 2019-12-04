from django.shortcuts import render, get_object_or_404
from .models import Customer, Object, ObjTr
from django.db.models import Q
from django.views.generic import View
from django.utils import timezone
from .render import Render
import datetime


def index(request):
    customers = Customer.objects.all().order_by('month_id', 'kunde', 'bpoststed')
    query = request.GET.get("q")
    all = request.GET.get("a")

    if query:
        customers = customers.filter(
            Q(kunde__icontains=query)).order_by('kunde', 'bpoststed')
    if all:
        customers = Customer.objects.all().order_by('kunde', 'bpoststed')

    context = {
        'customers': customers,
        'query': query,
        'all': all,
    }
    return render(request, 'index.html', context)


def detail(request, pk):
    custpk = request.POST.get("custpk")
    toast = request.POST.get("toast")
    if custpk:
        obj = Object.objects.get(pk=pk)
        customer = obj.customer
    else:
        customer = Customer.objects.get(pk=pk)
        obj = ""

    objects = Object.objects.filter(customer=customer).order_by("etg", "refnr")

    if toast == "kontroll":
        objtr = ObjTr(object=obj, customer=obj.customer, kontrolldato=timezone.now())
        objtr.save()
        obj.sistekontroll = timezone.now().year
        obj.save()

    if toast == "service":
        objtr = ObjTr(object=obj, customer=obj.customer, servicedato=timezone.now(), kontrolldato=timezone.now())
        objtr.save()
        obj.sisteservice = timezone.now().year
        obj.sistekontroll = timezone.now().year
        obj.save()

    context = {
        "customer": customer,
        "obj": obj,
        "toast": toast,
        "objects": objects,
        }
    return render(request, "detail.html", context)


def obj_detail(request, pk):
    obj = Object.objects.get(pk=pk)
    customer = obj.customer
    kontroll = request.GET.get("kontroll")
    service = request.GET.get("service")
    endring = request.GET.get("endring")
    avvik = request.GET.get("avvik")
    if kontroll == "now":
        objtr = ObjTr(object=obj, customer=obj.customer, kontrolldato=timezone.now())
        objtr.save()
        obj.sistekontroll = timezone.now().year
        obj.save()

    if service == "now":
        objtr = ObjTr(object=obj, customer=obj.customer, servicedato=timezone.now())
        objtr.save()
        obj.sisteservice = timezone.now().year
        obj.save()

    context = {
        "customer": customer,
        "obj": obj,
        "kontroll": kontroll,
        "service": service,
        "endring": endring,
        "avvik": avvik,
    }

    return render(request, "obj_detail.html", context)


def objtr(request, pk):
    customer = Customer.objects.get(pk=pk)
    objs = customer.objtr_set.all()
    context = {
        "customer": customer,
        "objs": objs,
    }
    return render(request, "objtr.html", context)


def test(request):
    return render(request, 'test.html', {})


class Pdf(View):

    def get(self, request, pk):
        customer = Customer.objects.get(pk=pk)
        objs = customer.objtr_set.all()
        kontrs = objs.exclude(kontrolldato=None)
        services = objs.exclude(servicedato=None)
        today = timezone.now()
        context = {
            "customer": customer,
            "today": today,
            "objs": objs,
            "kontrs": kontrs,
            "services": services,
        }
        return Render.render('pdf.html', context)
