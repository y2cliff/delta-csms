from django.contrib import admin
from . import models
from import_export import resources
from import_export.fields import Field
from import_export.widgets import DecimalWidget


class SiteAdmin(admin.ModelAdmin):
    list_display=['code','name']
    readonly_fields = ('date_created', 'date_updated', 'created_by', 'updated_by')


class BudgetItemAdmin(admin.ModelAdmin):
    list_display=['code','name','site']
    readonly_fields = ('date_created', 'date_updated')

    
class ActivityAdmin(admin.ModelAdmin):
    list_display=['code','name','leader']
    readonly_fields = ('date_created', 'date_updated')

    
class ProjCategoryAdmin(admin.ModelAdmin):
    list_display=['code','name']
    readonly_fields = ('date_created', 'date_updated')


class TaskAdmin(admin.ModelAdmin):
    list_display=['activity','code','name','leader']
    readonly_fields = ('date_created', 'date_updated')


class DashboardAdmin(admin.ModelAdmin):
    list_display=['user']
    readonly_fields = ('date_created', 'date_updated', 'created_by', 'updated_by')

class UserWorkDateAdmin(admin.ModelAdmin):
    list_display=['user']
    readonly_fields = ('date_created', 'date_updated', 'created_by', 'updated_by')

class DailyWorkAdmin(admin.ModelAdmin):
    list_display=['workdate']
    readonly_fields = ('date_created', 'date_updated', 'created_by', 'updated_by')

class SiteResource(resources.ModelResource):
    code = Field(column_name='Code')
    name = Field(column_name='Name')


    class Meta:
        model = models.Site
        fields = export_order = ('code', 'name')

    def dehydrate_code(self, obj):
        return obj.code

    def dehydrate_name(self, obj):
        return obj.name


class BudgetItemResource(resources.ModelResource):
    code = Field(column_name='Code')
    name = Field(column_name='Name')
    site = Field(column_name='Site')
    type = Field(column_name='Type')
    amount = Field(column_name='Amount')


    class Meta:
        model = models.BudgetItem
        fields = export_order = ('code', 'name', 'site', 'type', 'amount')

    def dehydrate_code(self, obj):
        return obj.code

    def dehydrate_name(self, obj):
        return obj.name

    def dehydrate_site(self, obj):
        return obj.site.code

    def dehydrate_type(self, obj):
        return obj.type

    def dehydrate_amount(self, obj):
        return obj.amount


class ProjCategoryResource(resources.ModelResource):
    code = Field(column_name='Code')
    name = Field(column_name='Name')

    class Meta:
        model = models.ProjCategory
        fields = export_order = ('code', 'name')

    def dehydrate_code(self, obj):
        return obj.code

    def dehydrate_name(self, obj):
        return obj.name


class WorkResource(resources.ModelResource):
    code = Field(column_name='Code')
    description = Field(column_name='Description')

    class Meta:
        model = models.Work
        fields = export_order = ('code', 'description')

    def dehydrate_code(self, obj):
        return obj.code

    def dehydrate_description(self, obj):
        return obj.description


class ActivityResource(resources.ModelResource):
    code = Field(column_name='Code')
    name = Field(column_name='Name')
    site = Field(column_name='Site')
    start_date = Field(column_name='Type')
    leader = Field(column_name='Amount')


    class Meta:
        model = models.Activity
        fields = export_order = ('code', 'name', 'site', 'start_date', 'leader')

    def dehydrate_code(self, obj):
        return obj.code

    def dehydrate_name(self, obj):
        return obj.name

    def dehydrate_site(self, obj):
        return obj.site

    def dehydrate_start_date(self, obj):
        return obj.start_date

    def dehydrate_leader(self, obj):
        return obj.leader


class TaskResource(resources.ModelResource):
    sequence = Field(column_name='Sequence')
    code = Field(column_name='Code')
    name = Field(column_name='Name')
    activity = Field(column_name='Activity')
    budget_item = Field(column_name='Budget Item')
    leader = Field(column_name='Leader')


    class Meta:
        model = models.Task
        fields = export_order = ('sequence', 'code', 'name', 'activity', 'budget_item', 'leader')

    def dehydrate_sequence(self, obj):
        return obj.sequence

    def dehydrate_code(self, obj):
        return obj.code

    def dehydrate_name(self, obj):
        return obj.name

    def dehydrate_activity(self, obj):
        return obj.activity

    def dehydrate_budget_item(self, obj):
        return obj.type

    def dehydrate_leader(self, obj):
        return obj.leader


admin.site.register(models.Site,SiteAdmin)
admin.site.register(models.BudgetItem,BudgetItemAdmin)
admin.site.register(models.Activity,ActivityAdmin)
admin.site.register(models.Task,TaskAdmin)
admin.site.register(models.ProjCategory,ProjCategoryAdmin)
admin.site.register(models.ProjDashboard,DashboardAdmin)

admin.site.register(models.UserWorkDate,UserWorkDateAdmin)
admin.site.register(models.DailyWork,DailyWorkAdmin)
 