from django import forms
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect
from .models import Slokketype, Object, Customer, ObjTr, Avvik, Extinguishant, Extra
from django.utils import timezone
from django.forms.widgets import CheckboxSelectMultiple, SelectMultiple, Textarea
from django.utils.safestring import mark_safe

class DateInput(forms.DateInput):
    input_type = 'date'

class NyObjectForm(forms.ModelForm):
    extinguishant = forms.ModelChoiceField(queryset=Extinguishant.objects.order_by('fabrikat', 'type', 'slukkemiddel', 'lengde'))
    class Meta:
        model = Object
        fields = ['extinguishant', 'prodyear', 'sisteservice','nesteservice', 'lokasjon', 'plassering', 'etg']
        widgets = {
            'sisteservice': DateInput,
            'nesteservice': DateInput
        }

class AvvikForm(forms.ModelForm):
    class Meta:
        model = ObjTr
        fields = ['avvik', 'kommentar']
        widgets = {
            'avvik': CheckboxSelectMultiple(
            ),
            'kommentar': Textarea(
                attrs={
                    'rows': 4, 'cols': 50
                })
        }


class ExtraForm(forms.ModelForm):
    beskrivelse = forms.ModelChoiceField(Extra.objects.all())
    class Meta:
        model = Extra
        fields = ['beskrivelse']