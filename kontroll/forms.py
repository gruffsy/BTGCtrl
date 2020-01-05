from django import forms
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect
from .models import Slokketype, Object, Customer, ObjTr, Avvik
from django.utils import timezone
from django.forms.widgets import CheckboxSelectMultiple, SelectMultiple



class NyObjectForm(forms.ModelForm):
    class Meta:
        model = Object
        fields = ['extinguishant', 'prodyear', 'lokasjon', 'plassering', 'etg']

class AvvikForm(forms.ModelForm):
    class Meta:
        model = ObjTr
        fields = ['avvik']
