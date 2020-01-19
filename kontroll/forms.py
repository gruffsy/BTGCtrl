from django import forms
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect
from .models import Slokketype, Object, Customer, ObjTr, Avvik, Extinguishant
from django.utils import timezone
from django.forms.widgets import CheckboxSelectMultiple, SelectMultiple, Textarea
from django.utils.safestring import mark_safe


class NyObjectForm(forms.ModelForm):
    extinguishant = forms.ModelChoiceField(queryset=Extinguishant.objects.order_by('fabrikat', 'type', 'slukkemiddel', 'lengde'))

    class Meta:
        model = Object
        fields = ['extinguishant', 'prodyear', 'lokasjon', 'plassering', 'etg']


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
