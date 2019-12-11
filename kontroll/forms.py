from django import forms
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from .models import Slokketype


class NySlokketypeForm(forms.ModelForm):
    class Meta:
        model = Slokketype
        fields = ['navn', 'intervall']


def contact(request):
    submitted = False
    if request.method == 'POST':
        form = NySlokketypeForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            album = form.save(commit=False)
            album.save()
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
