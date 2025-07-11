from base.scaffolding import CrudManager, ChildCrudManager
from base.views import TemplateChildCreateView, TemplateChildDeleteView
# from xystum import syscode
from .forms import ManufacturerForm, RadioForm, RadioLicenseForm
from .models import Manufacturer, Radio, RadioLicense
from .tables import ManufacturerTable, RadioTable, RadioLicenseTable
from .filters import ManufacturerFilter, RadioFilter, RadioLicenseFilter
from .admin import ManufacturerResource, RadioResource, RadioLicenseResource


class ManufacturerCrudManager(CrudManager):
    page_title = 'Manufacturer'
    parent_menu = [["CIT",'cit:home'],["Manufacturer",'cit:manufacturer-list']]
    page_name = 'List'
    form_class = ManufacturerForm
    model = Manufacturer
    table_class = ManufacturerTable
    module = 'cit'
    model_resource = ManufacturerResource
    

class RadioCrudManager(CrudManager):
    page_title = 'Radio'
    parent_menu = [["CIT",'cit:home'],["Radio",'cit:radio-list']]
    page_name = 'List'
    form_class = RadioForm
    filterset_class = RadioFilter
    model = Radio
    table_class = RadioTable
    module = 'cit'
    model_resource = RadioResource


class RadioLicenseCrudManager(CrudManager):
    page_title = 'Radio License'
    parent_menu = [["CIT",'cit:home'],["Radio License",'cit:radiolicense-list']]
    page_name = 'List'
    form_class = RadioLicenseForm
    model = RadioLicense
    table_class = RadioLicenseTable
    module = 'cit'
    model_resource = RadioLicenseResource


# class RadioLicenseChildCrudManager(ChildCrudManager):
#     parent_model = Radio
#     page_title = 'Radio License'
#     parent_menu = [["cit",'cit:home'], ["Radio License",'cit:radiolicense-list']]
#     page_name = 'List'
#     form_class = RadioLicenseForm
#     model = RadioLicense
#     table_class = RadioLicenseTable
#     module = 'cit'
#     # model_resource = ActivityResource
