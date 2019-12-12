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

class EndreObjectForm(forms.ModelForm):
    class Meta:
        model = Object
        fields = ['lokasjon', 'plassering', 'etg']

