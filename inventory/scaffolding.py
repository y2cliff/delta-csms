from base.scaffolding import CrudManager, ChildCrudManager
from base.views import TemplateChildCreateView, TemplateChildDeleteView
# from xystum import syscode
from . import forms
from . import models
from . import tables
from . import filters
from . import admin


class InvCategoryCrudManager(CrudManager):
    page_title = 'Inventory Category'
    parent_menu = [["Inventory",'inventory:home'],["Category",'inventory:invcategory-list']]
    page_name = 'Inventory Category'
    form_class = forms.InvCategoryForm
    model = models.InvCategory
    table_class = tables.InvCategoryTable
    filterset_class = filters.InvCategoryFilter
    module = 'inventory'
    model_resource = admin.InvCategoryResource
