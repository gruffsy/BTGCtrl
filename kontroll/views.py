from django.shortcuts import render, get_object_or_404
from .models import Customer, Object
from django.db.models import Q


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
    customer = Customer.objects.get(pk=pk)
    objects = Object.objects.filter(customer=customer).order_by("etg", "refnr")
    context = {
        "customer": customer,
        "objects": objects,
    }

    return render(request, "detail.html", context)


def obj_detail(request, pk):
    obj = Object.objects.get(pk=pk)
    customer = obj.customer
    context = {
        "customer": customer,
        "obj": obj,
    }

    return render(request, "obj_detail.html", context)


def test(request):
    return render(request, 'test.html', {})
