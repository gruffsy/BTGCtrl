from django.db import models
from datetime import datetime, date
# Create your models here.

class Month(models.Model):
    navn = models.CharField(max_length=20)
    intervall = models.PositiveSmallIntegerField(default=5)

    def __str__(self):
        return self.navn

class Customer(models.Model):
    kunde = models.CharField(max_length=255)
    kundeinformasjon = models.CharField(max_length=255, null=True, blank=True)
    badresse = models.CharField(max_length=255, null=True, blank=True)
    bpostnr = models.PositiveSmallIntegerField(null=True, blank=True)
    bpoststed = models.CharField(max_length=255, null=True, blank=True)
    fadresse = models.CharField(max_length=255, null=True, blank=True)
    fpostnr = models.PositiveSmallIntegerField(null=True, blank=True)
    fpoststed = models.CharField(max_length=255, null=True, blank=True)
    kontaktperson = models.CharField(max_length=255, null=True, blank=True)
    tlf1 = models.PositiveIntegerField(null=True, blank=True)
    tlf2 = models.PositiveIntegerField(null=True, blank=True)
    nummer = models.PositiveIntegerField(null=True, blank=True)
    tripletex = models.PositiveIntegerField(null=True, blank=True)
    email = models.CharField(max_length=255, null=True, blank=True)
    kommentar = models.TextField(null=True, blank=True)
    month = models.ForeignKey(Month, on_delete=models.CASCADE)
    aktiv = models.BooleanField(default=True)

    def __str__(self):
        return self.kunde + ' | ' + self.badresse + ' | ' + self.bpoststed


class Slokketype(models.Model):
    navn = models.CharField(max_length=255)

    def __str__(self):
        return self.navn

class Extinguishant(models.Model):
    fabrikat = models.CharField(max_length=255, null=True, blank=True)
    type = models.CharField(max_length=255, null=True, blank=True)
    lengde = models.CharField(max_length=255, null=True, blank=True)
    slukkemiddel = models.CharField(max_length=255, null=True, blank=True)
    slokketype = models.ForeignKey(Slokketype, on_delete=models.CASCADE)


    def __str__(self):
        return self.fabrikat + ' | ' + self.type

class Object(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    lokasjon = models.CharField(max_length=255, null=True, blank=True)
    etg = models.CharField(max_length=255, null=True, blank=True)
    plassering = models.CharField(max_length=255, null=True, blank=True)
    prodyear = models.PositiveSmallIntegerField(default=2010, blank=True)
    extinguishant = models.ForeignKey(Extinguishant, on_delete=models.CASCADE)
    sisteservice = models.DateField(null=True, blank=True)
    sistekontroll = models.DateField(null=True, blank=True)
    nesteservice = models.DateField(null=True, blank=True)
    nestekontroll = models.DateField(null=True, blank=True)
    avvik = models.BooleanField(default=False)
    aktiv = models.BooleanField(default=True)
    def __str__(self):
        return self.lokasjon + ' | ' + self.plassering + ' | ' + self.etg + ' | ' + self.extinguishant.fabrikat


class ObjTr(models.Model):
    object = models.ForeignKey(Object, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    kontrolldato = models.DateField(null=True, blank=True)
    servicedato = models.DateField(null=True, blank=True)
    avvik = models.BooleanField(default=False)

    def __str__(self):
        return self.object.extinguishant.fabrikat + ' | ' + self.customer.kunde


class Avvik(models.Model):
    avvik = models.TextField()
    slokketype = models.ManyToManyField('Slokketype')

    def __str__(self):
        return str(self.avvik)
