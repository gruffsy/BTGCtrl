from django.shortcuts import render, get_object_or_404, redirect
from .models import Customer, Object, ObjTr, Slokketype
from django.db.models import Q
from django.views.generic import View
from django.utils import timezone
from datetime import date
import os
from django.conf import settings
from django.http import HttpResponse
from django.template import Context
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from .forms import NyObjectForm


def link_callback(uri, rel):
    """
    Convert HTML URIs to absolute system paths so xhtml2pdf can access those
    resources
    """
    # use short variable names
    sUrl = settings.STATIC_URL  # Typically /static/
    sRoot = settings.STATIC_ROOT  # Typically /home/userX/project_static/
    mUrl = settings.MEDIA_URL  # Typically /static/media/
    mRoot = settings.MEDIA_ROOT  # Typically /home/userX/project_static/media/

    # convert URIs to absolute system paths
    if uri.startswith(mUrl):
        path = os.path.join(mRoot, uri.replace(mUrl, ""))
    elif uri.startswith(sUrl):
        path = os.path.join(sRoot, uri.replace(sUrl, ""))
    else:
        return uri  # handle absolute uri (ie: http://some.tld/foo.png)

    # make sure that file exists
    if not os.path.isfile(path):
        raise Exception(
            'media URI must start with %s or %s' % (sUrl, mUrl)
        )
    return path


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
    custpk = request.GET.get("custpk")
    toast = request.GET.get("toast")
    aktiv = request.GET.get('aktiv')

    if custpk:
        obj = Object.objects.get(pk=pk)
        customer = obj.customer

    else:
        customer = Customer.objects.filter(pk=pk)[0]
        obj = None

    objects = Object.objects.filter(customer=customer, aktiv=True).order_by("etg", "plassering")
    lokasjon = objects.values_list('lokasjon', flat=True).last()
    etg = objects.values_list('etg', flat=True).last()
    plassering = objects.values_list('plassering', flat=True).last()
    submitted = False
    exts = Slokketype.objects.all()

    if toast == "kontroll":
        objtr = ObjTr(object=obj, customer=obj.customer, kontrolldato=timezone.now())
        objtr.save()
        obj.sistekontroll = timezone.now()
        obj.save()

    if toast == "endring":
        obj.etg = request.GET['etg']
        obj.lokasjon = request.GET['lokasjon']
        obj.plassering = request.GET['plassering']
        if aktiv:
            obj.aktiv = False
            objtr = ObjTr(object=obj, customer=obj.customer, kontrolldato=timezone.now(), avvik=True)
            objtr.save()

        obj.save()

    if toast == "service":
        objtr = ObjTr(object=obj, customer=obj.customer, servicedato=timezone.now(), kontrolldato=timezone.now())
        objtr.save()
        obj.sisteservice = timezone.now()
        obj.sistekontroll = timezone.now()
        obj.nesteservice = date(timezone.now().year + 5, timezone.now().month, timezone.now().day)
        obj.nestekontroll = date(timezone.now().year + 1, timezone.now().month, timezone.now().day)
        obj.save()

    if request.method == 'POST':
        form = NyObjectForm(request.POST or None)
        if form.is_valid():
            objform = form.save(commit=False)
            objform.customer = customer
            objform.save()
            # return redirect('../' + str(pk) + '?submitted=True')
    else:
        form = NyObjectForm(
            initial={'lokasjon': lokasjon, 'etg': etg, 'plassering': plassering,
                     'prodyear': int(timezone.now().year)})
        if 'submitted' in request.GET:
            submitted = True
    context = {
        "customer": customer,
        "obj": obj,
        "toast": toast,
        "objects": objects,
        "exts": exts,
        'form': form,
        'custpk': custpk,
        'submitted': submitted,
        'pk': pk,
        'aktiv': aktiv,
    }
    return render(request, "detail.html", context)


def nyobject(request):
    pass


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
    objs = customer.objtr_set.all().filter(avvik=False).order_by('-kontrolldato')
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
    return render(request, "objtr.html", context)


def test(request):
    return render(request, 'test.html', {})


class Pdf(View):

    def get(self, request, pk):
        month = request.GET.get("month")
        month = month[-4:]
        customer = Customer.objects.get(pk=pk)
        objs = customer.objtr_set.all().filter(kontrolldato__year=month)
        kontrs = objs.exclude(kontrolldato=None)
        services = objs.exclude(servicedato=None)
        today = timezone.now()
        context = {
            "customer": customer,
            "today": today,
            "objs": objs,
            "kontrs": kontrs,
            "services": services,
            "month": month,
        }
        template_path = 'pdf.html'

        # Create a Django response object, and specify content_type as pdf
        response = HttpResponse(content_type='application/pdf')
        template = get_template(template_path)
        html = template.render(context)
        # create a pdf
        pisaStatus = pisa.CreatePDF(
            html, dest=response, link_callback=link_callback)

        return response

    # return Render.render('pdf.html', context)
