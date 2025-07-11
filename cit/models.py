from base.abstract import TemplateModel
from project.models import Site
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum, F
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
import datetime


class CitDashboard(TemplateModel):
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='cit_dashboard',
    )

class Manufacturer(TemplateModel):
    code = models.CharField(
        max_length=10, 
        unique=True, 
        error_messages={'unique': "Code has already been used."}
    )
    name = models.CharField(max_length=60, blank=True, null=True)

    class Meta:
        ordering = ["code"]
        permissions = (
            ('delete_foreign_manufacturer', _('Can delete foreign manufacturer')),
        )

    def __str__(self):
        return self.code

    def get_absolute_url(self):
        return reverse('cit:manufacturer-detail',kwargs={'pk': self.id})


class Radio(TemplateModel):
    BAND_TYPE = (
        ('VHF','VHF'),
        ('350','350'),
        ('UHF','UHF'),
    )
    RADIO_TYPE = (
        ('P','Portable'),
        ('F','Fixed Base'),
        ('M','Mobile Base'),
        ('R','Repeater')
    )
    RADIO_STATUS = (
        ('OK','Active'),
        ('DEFECT','Defective'),
        ('STORE','Storaged'),
        ('DISPOSE','Disposed')
    )
    serial_number = models.CharField(
        max_length=30, 
        unique=True, 
        error_messages={'unique': "Code has already been used."}
    )
    manufacturer = models.ForeignKey('Manufacturer', on_delete=models.PROTECT, blank=True, null=True, related_name='radios')
    model = models.CharField(max_length=60, blank=True, null=True)
    status = models.CharField(max_length=10, default="Admin", choices=RADIO_STATUS)
    site = models.ForeignKey(Site, on_delete=models.PROTECT, blank=True, null=True, related_name='radios')
    frequency_band = models.CharField(max_length=3, default="UHF", choices=BAND_TYPE)
    frequency = models.CharField(max_length=60, blank=True, null=True)
    type = models.CharField(max_length=1, default="OK", choices=RADIO_TYPE)
    amount = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    purchased_date = models.DateField(blank=True, null=True)


    class Meta:
        ordering = ["serial_number"]
        permissions = (
            ('delete_foreign_radio', _('Can delete foreign radio')),
        )

    def __str__(self):
        return self.serial_number

    def get_absolute_url(self):
        return reverse('cit:radio-detail',kwargs={'pk': self.id})


class RadioLicense(TemplateModel):
    LICENSE_TYPE = (
        ('N','New'),
        ('R','Renewal'),
        ('S','Storage')
    )
    radio = models.ForeignKey('Radio', on_delete=models.PROTECT, blank=True, null=True, related_name='licenses')
    license_number = models.CharField(max_length=60, blank=True, null=True)
    effective_date = models.DateField(blank=True, null=True)
    expiry_date = models.DateField(blank=True, null=True)
    type = models.CharField(max_length=1, default="Admin", choices=LICENSE_TYPE)


    class Meta:
        ordering = ["license_number"]
        permissions = (
            ('delete_foreign_radio', _('Can delete foreign radio')),
        )

    def __str__(self):
        return self.radio + ' - ' + self.license_number

    def get_absolute_url(self):
        return reverse('cit:radiolicense-detail',kwargs={'pk': self.id})