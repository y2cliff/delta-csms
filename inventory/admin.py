from django.contrib import admin
from .models import InvCategory
from import_export import resources
from import_export.fields import Field
from import_export.widgets import DecimalWidget


class InvCategoryAdmin(admin.ModelAdmin):
    list_display=['code','name']
    readonly_fields = ('date_created', 'date_updated', 'created_by', 'updated_by')

class InvCategoryResource(resources.ModelResource):
    code = Field(column_name='Code')
    name = Field(column_name='Name')

    class Meta:
        model = InvCategory
        fields = export_order = ('code', 'name', 'created_by', 'date_created', 'updated_by', 'date_updated')

    def dehydrate_code(self, obj):
        return obj.code

    def dehydrate_name(self, obj):
        return obj.name

admin.site.register(InvCategory,InvCategoryAdmin)