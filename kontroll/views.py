from .models import Object, ObjTr, Avvik, Customer, Month, Slokketype, Extinguishant
from django.db.models import Q
from django.views.generic import View
from django.utils import timezone
from datetime import date, timedelta
import os
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import NyObjectForm, AvvikForm
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets
from rest_framework import permissions
from .serializer import ObjectSerializer, ObjTrSerializer, AvvikSerializer, CustomerSerializer, MonthSerializer, \
    SlokketypeSerializer, ExtinguishantSerializer


@login_required(login_url='/accounts/login/')
def index(request):
    query = request.GET.get("q")
    sort = request.GET.get("sort")
    alle = request.GET.get("a")
    medavvik = request.GET.get("medavvik")
    if medavvik == 'true':
        medavvik = True
    else:
        medavvik = False

    # utvid = request.GET.get("utvid")
    kontroll = []
    
    dager = 150
    time_threshold = timezone.now() - timedelta(days=dager)
    customers = Customer.objects.filter(aktiv=True)
    for c in customers:
        objs = Object.objects.filter(customer=c, aktiv=True, avvik=medavvik)
        objs = objs.filter(Q(sistekontroll__lte=time_threshold) | Q(sistekontroll=None))
        if objs:
            kontroll.append(c.pk)
    customers = customers.filter(pk__in=kontroll).order_by('month_id')
    if alle:
        customers = Customer.objects.filter(aktiv=True)

    if query:
        customers = Customer.objects.all().filter(
            Q(kunde__icontains=query)).order_by('month_id', 'kunde', 'bpoststed')
    if sort:
        customers = customers.order_by(sort)

    context = {
        'customers': customers,
        'query': query,
        'all': alle,
        'sort': sort,
        'kontroll': kontroll,
        'medavvik': medavvik,

    }
    return render(request, 'index.html', context)


@login_required(login_url='/accounts/login/')
def detail(request, pk):
    custpk = request.POST.get("custpk")
    # Henter custpk fra endringer gjort med objekt. Ingen endringer. Custpk=pk fra url
    toast = request.POST.get("toast")
    avvik = request.POST.get('avvik')
    detalj = request.POST.get('detalj')
    utsett = request.POST.get('utsett')
    
    aktiv = request.GET.get('aktiv')
    liste = request.GET.get('liste')
    today = int(timezone.now().year)
    nyobject = request.GET.get('nyobject')
    book = request.GET.get('book')
    objtrid = request.GET.get('objtrid')
    action = request.GET.get('action')

    if nyobject:
        toast = 'nyobject'

    if avvik is None and toast == 'avvik':
        toast = 'kontroll'

    if custpk:
        obj = Object.objects.get(pk=pk)
        customer = obj.customer

    else:
        customer = Customer.objects.filter(pk=pk)[0]
        obj = request.GET.get('obj') or None
        if obj is not None:
            obj = Object.objects.filter(pk=int(obj))[0]
        custpk = customer.pk

    dager = 150
    time_threshold = timezone.now() - timedelta(days=dager)
    objects = Object.objects.filter(customer=customer, aktiv=True).order_by("etg", "lokasjon", "plassering")
    bookings = ObjTr.objects.filter(customer=customer, status=2).order_by('-pk')
    tot_ant_obj = objects.count()
    ant_obj = tot_ant_obj
    # Usikker på hva avviks brukes til, kan kanskje slettes
    avviks = objects.exclude(avvik=None).count()
    if not liste:
        objects = objects.filter(
            Q(sistekontroll__lte=time_threshold) | Q(sistekontroll=None) | Q(nesteservice__lte=timezone.now()))
        ant_obj = objects.count()

    if toast == "kontroll":
        # lagrer kontrolldato i objektTransaksjoner
        objtr = ObjTr(object=obj, customer=obj.customer, kontrolldato=timezone.now(), user=request.user, status=2)
        objtr.save()
        # oppdaterer objektet med nye kontrolldatoer
        obj.sistekontroll = timezone.now()
        obj.nestekontroll = date(timezone.now().year + 1, timezone.now().month, timezone.now().day)
        obj.save()

    if toast == "endring":
        obj.etg = request.POST['etg']
        obj.lokasjon = request.POST['lokasjon']
        obj.plassering = request.POST['plassering']
        obj.prodyear = request.POST['prodyear']
        obj.sisteservice = request.POST['sisteservice'] or None
        obj.nesteservice = request.POST['nesteservice'] or None
        obj.save()

    if toast == "slette":
        obj.aktiv = False
        obj.status = 2
        obj.save()
        objtr = ObjTr(object=obj, customer=obj.customer, deleted=True, user=request.user, status=2)
        objtr.save()

    if toast == 'utsett':
        obj.nesteservice = date(int(utsett), timezone.now().month, timezone.now().day)
        obj.save()

    if toast == "service":
        objtr = ObjTr(object=obj, customer=obj.customer, servicedato=timezone.now(), user=request.user, status=2)
        objtr.save()
        obj.sisteservice = timezone.now()
        obj.nesteservice = date(timezone.now().year + obj.extinguishant.slokketype.intervall, timezone.now().month,
                                timezone.now().day)
        # trengs nestekontroll?
        obj.nestekontroll = date(timezone.now().year + 1, timezone.now().month, timezone.now().day)
        obj.save()


    if book == "yes":
        ObjTr.objects.filter(pk=objtrid).update(status=1)
    elif book == "no":
        objtrbooking = ObjTr.objects.get(pk=objtrid)
        if action == 'kontroll':
            objtrbooking.object.sistekontroll = date(timezone.now().year - 1, timezone.now().month, timezone.now().day)
        if action == 'service':
            objtrbooking.object.sisteservice = date(timezone.now().year - 1, timezone.now().month, timezone.now().day)
            objtrbooking.object.nesteservice = timezone.now()
        if action == 'avvik':
            objtrbooking.object.avvik = False
        if action == 'utbedret':
            pass
        if action == 'added':
            objtrbooking.object.aktiv = False
        if action == 'deleted':
            objtrbooking.object.aktiv = True
        objtrbooking.object.save()
        objtrbooking.delete()
    elif book == 'all':
        ob = ObjTr.objects.filter(customer=customer, status=2)
        ob.update(status=1)

    slettet = Object.objects.filter(customer=customer, aktiv=False).order_by("modified")
    lokasjon = slettet.values_list('lokasjon', flat=True).last()
    etg = slettet.values_list('etg', flat=True).last()
    plassering = slettet.values_list('plassering', flat=True).last()
    nesteservice = slettet.values_list('nesteservice', flat=True).last()
    sisteservice = slettet.values_list('sisteservice', flat=True).last()

    if request.method == 'POST':
        if avvik is not None:
            avvikform = AvvikForm(request.POST or None)
            objform = avvikform.save(commit=False)
            objform.customer = obj.customer
            objform.object = obj
            objform.user = request.user
            objform.status = 2
            objform.save()
            obj.avvik = True
            obj.save()
            avvikform.save_m2m()
            nyform = NyObjectForm(
                initial={'lokasjon': lokasjon, 'etg': etg, 'plassering': plassering, 'nesteservice': nesteservice, 'sisteservice':sisteservice,
                         'prodyear': int(timezone.now().year)} )
        else:
            nyform = NyObjectForm(request.POST or None)
            avvikform = AvvikForm()
            if nyform.is_valid():
                objform = nyform.save(commit=False)
                objform.customer = customer
                # lagrer informasjon om neste service !!!!VIKTIG!!!
                #objform.nesteservice = str(objform.prodyear + objform.extinguishant.slokketype.intervall) + '-' + str(
                #timezone.now().month) + '-01'
                objform.save()
                objtr = ObjTr(object=Object.objects.last(), customer=customer, added=True, user=request.user, status=2)
                objtr.save()
                nyobject = True
                toast = 'nyobject'

    else:
        nyform = NyObjectForm(
            initial={'lokasjon': lokasjon, 'etg': etg, 'plassering': plassering, 'nesteservice': nesteservice, 'sisteservice':sisteservice,
                     'prodyear': int(timezone.now().year)})
        avvikform = AvvikForm()
        if obj is not None:
            avvikform.fields["avvik"].queryset = Avvik.objects.filter(slokketype=obj.extinguishant.slokketype).order_by(
                'id')



    context = {
        "customer": customer,
        "obj": obj,
        "toast": toast,
        "objects": objects,
        'nyform': nyform,
        'avvikform': avvikform,
        'custpk': custpk,
        'pk': pk,
        'aktiv': aktiv,
        'avvik': avvik,
        'avviks': avviks,
        'liste': liste,
        'tot_ant_obj': tot_ant_obj,
        'ant_obj': ant_obj,
        'detalj': detalj,
        'today': today,
        'utsett': utsett,
        'nyobject': nyobject,
        'bookings': bookings,
    }
    return render(request, "detail.html", context)


@login_required(login_url='/accounts/login/')
def avvik(request, pk):
    obj = request.GET.get('obj') or None
    remove = request.GET.get('remove')
    avvik = request.GET.get('avvik') or None
    kommentar = request.POST.get('kommentar') or None
    oppdatert = request.GET.get('oppdatert') or None

    if obj:
        obj = Object.objects.get(pk=obj, aktiv=True)
        objtr = ObjTr.objects.get(object=obj, kontrolldato=None, utbedret_avvik=None, object__aktiv=True, deleted=False,
                                  added=False, servicedato=None)
        avviks = objtr.avvik.all()
        customer = objtr.customer
        if kommentar is None:
            kommentar = objtr.kommentar
            oppdatert = None

    else:
        objtr = ObjTr.objects.filter(customer=pk, kontrolldato=None, utbedret_avvik=None, object__aktiv=True,
                                     deleted=False, added=False, servicedato=None)
        avviks = 'False'
        customer = Customer.objects.get(pk=pk)

    if kommentar:
        objtr.kommentar = kommentar
        objtr.save()


    if remove is not None:
        objtr.avvik.remove(avvik)
        avvik_id = Avvik.objects.get(pk=str(avvik))
        avviktr = ObjTr(object=obj, utbedret_avvik=avvik_id, customer=customer, kommentar=kommentar, user=request.user,
                        status=2)
        avviktr.save()

    context = {
        'objtr': objtr,
        'obj': obj,
        'pk': pk,
        'avviks': avviks,
        "customer": customer,
        'kommentar': kommentar,
        'oppdatert': oppdatert,
    }

    # alle avvik er lukket
    if not avviks:
        obj.avvik = False
        obj.sistekontroll = timezone.now()
        obj.save()
        objtr.delete()
        objtr = ObjTr(object=obj, customer=obj.customer, kontrolldato=timezone.now(), status=2)
        objtr.save()
        url = '../' + str(pk)

        return HttpResponseRedirect(url)
    else:

        return render(request, "avvik.html", context)


@login_required(login_url='/accounts/login/')
def objtr(request, pk):
    customer = Customer.objects.get(pk=pk)
    objs = ObjTr.objects.filter(customer=customer).order_by('-modified')
    bookings = ObjTr.objects.filter(customer=customer, status=2)
    context = {
        "customer": customer,
        "objs": objs,
        "bookings": bookings,
    }
    return render(request, "objtr.html", context)

class Pdf(View):
    def get(self, request, pk):
        year = request.GET.get("year")
        customer = Customer.objects.get(pk=pk)
        objs = ObjTr.objects.filter(customer=customer, status=1)
        objs = objs.filter(modified__year=year)
        objs = objs.order_by('object_id')
        services = objs.exclude(servicedato=None)
        kontr = objs.filter(servicedato=None, utbedret_avvik=None)
        kontr = kontr.exclude(Q(added=True) | Q(deleted=True))
        kontrs = kontr.count()
        kontrslokkere = kontr.exclude(object__extinguishant__slokketype=3).count()
        kontrbrannposter = kontrs - kontrslokkere
        avviks = objs.exclude(avvik=None).count()
        utbedret_avviks = objs.exclude(utbedret_avvik=None).count()
        added = objs.exclude(added=False).count()
        deleted = objs.exclude(deleted=False).count()
        context = {
            "customer": customer,
            "objs": objs,
            "year": year,
            "services": services,
            "kontrs": kontrs,
            "avviks": avviks,
            "utbedret_avviks": utbedret_avviks,
            "added": added,
            "deleted": deleted,
            "kontrslokkere": kontrslokkere,
            "kontrbrannposter": kontrbrannposter,
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


class ObjectViewSet(viewsets.ModelViewSet):
    queryset = Object.objects.all()
    serializer_class = ObjectSerializer
    # permission_classes = [permissions.IsAuthenticated]


class ObjTrViewSet(viewsets.ModelViewSet):
    queryset = ObjTr.objects.all()
    serializer_class = ObjTrSerializer
    # permission_classes = [permissions.IsAuthenticated]


class MonthViewSet(viewsets.ModelViewSet):
    queryset = Month.objects.all()
    serializer_class = MonthSerializer
    # permission_classes = [permissions.IsAuthenticated]


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    # permission_classes = [permissions.IsAuthenticated]


class AvvikViewSet(viewsets.ModelViewSet):
    queryset = Avvik.objects.all()
    serializer_class = AvvikSerializer
    # permission_classes = [permissions.IsAuthenticated]


class SlokketypeViewSet(viewsets.ModelViewSet):
    queryset = Slokketype.objects.all()
    serializer_class = SlokketypeSerializer
    # permission_classes = [permissions.IsAuthenticated]


class ExtinguishanttViewSet(viewsets.ModelViewSet):
    queryset = Extinguishant.objects.all()
    serializer_class = ExtinguishantSerializer
    # permission_classes = [permissions.IsAuthenticated]
