from django import forms
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect
from .models import Slokketype, Object, Customer
from django.utils import timezone


class NySlokketypeForm(forms.ModelForm):
    class Meta:
        model = Slokketype
        fields = ['navn', 'intervall']


def nyslokketype(request):
    submitted = False
    if request.method == 'POST':
        form = NySlokketypeForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            slokketype = form.save(commit=False)
            slokketype.save()
            return HttpResponseRedirect('/contact?submitted=True')
    else:
        form = NySlokketypeForm()
        if 'submitted' in request.GET:
            submitted = True

    context = {
        'form': form,
        'submitted': submitted,

    }
    return render(request, 'contact.html', context)


class NyObjectForm(forms.ModelForm):
    class Meta:
        model = Object
        fields = ['extinguishant', 'prodyear', 'lokasjon', 'plassering', 'etg']


def nyobject(request, pk):
    customer = Customer.objects.filter(pk=pk)[0]
    obj = Object.objects.filter(customer=pk).all()
    lokasjon = obj.values_list('lokasjon', flat=True).last()
    etg = obj.values_list('etg', flat=True).last()
    plassering = obj.values_list('plassering', flat=True).last()
    submitted = False
    if request.method == 'POST':
        form = NyObjectForm(request.POST or None)
        if form.is_valid():
            objform = form.save(commit=False)
            objform.customer = customer
            objform.save()
            return redirect('../' + str(pk) + '?submitted=True')
    else:

        form = NyObjectForm(
            initial={'lokasjon': lokasjon, 'etg': etg, 'plassering': plassering, 'prodyear': int(timezone.now().year)})
        # form.fields['customer'].disabled = False

        if 'submitted' in request.GET:
            submitted = True

    context = {
        'form': form,
        'submitted': submitted,
        'pk': pk,
    }
    return render(request, 'contact.html', context)
