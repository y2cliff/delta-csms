from django.contrib import admin
from .models import Manufacturer, Radio, RadioLicense
from import_export import resources
from import_export.fields import Field
from import_export.widgets import DecimalWidget


class ManufacturerAdmin(admin.ModelAdmin):
    list_display=['code','name']
    readonly_fields = ('date_created','date_updated','created_by','updated_by')


class RadioAdmin(admin.ModelAdmin):
    list_display=['serial_number','manufacturer','model','site','type']
    readonly_fields = ('date_created','date_updated','created_by','updated_by')

    
class RadioLicenseAdmin(admin.ModelAdmin):
    list_display=['license_number','radio']
    readonly_fields = ('date_created','date_updated','created_by','updated_by')

    
class ManufacturerResource(resources.ModelResource):
    code = Field(column_name='Code')
    name = Field(column_name='Name')


    class Meta:
        model = Manufacturer
        fields = export_order = ('code', 'name')

    def dehydrate_code(self, obj):
        return obj.code

    def dehydrate_name(self, obj):
        return obj.name


class RadioResource(resources.ModelResource):
    serial_number = Field(column_name='Serial Number')
    manufacturer = Field(column_name='Name')
    model = Field(column_name='Model')
    site = Field(column_name='Site')
    type = Field(column_name='Type')
    


    class Meta:
        model = Radio
        fields = export_order = ('serial_number', 'manufacturer', 'model', 'site', 'type')

    def dehydrate_serial_number(self, obj):
        return obj.serial_number

    def dehydrate_manufacturer(self, obj):
        return obj.manufacturer

    def dehydrate_model(self, obj):
        return obj.model

    def dehydrate_type(self, obj):
        return obj.type

    def dehydrate_site(self, obj):
        return obj.site.code


class RadioLicenseResource(resources.ModelResource):
    license_number = Field(column_name='License Number')
    effective_date = Field(column_name='Effective Date')
    expiry_date = Field(column_name='Expiry Date')

    class Meta:
        model = RadioLicense
        fields = export_order = ('license_number', 'effective_date', 'expiry_date')

    def dehydrate_code(self, obj):
        return obj.code

    def dehydrate_name(self, obj):
        return obj.name


admin.site.register(Manufacturer,ManufacturerAdmin)
admin.site.register(Radio,RadioAdmin)
admin.site.register(RadioLicense,RadioLicenseAdmin)
 