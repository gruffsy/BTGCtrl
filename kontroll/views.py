from django.shortcuts import render
from .models import Customer

def index(request):
    customers = Customer.objects.all().order_by('month_id', 'kunde', 'bpoststed')
    context = {
        'customers': customers,
        }
    return render(request, 'index.html', context)
