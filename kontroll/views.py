from django.shortcuts import render, get_object_or_404
from .models import Customer, Object

def index(request):
    customers = Customer.objects.all().order_by('month_id', 'kunde', 'bpoststed')
    context = {
        'customers': customers,
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