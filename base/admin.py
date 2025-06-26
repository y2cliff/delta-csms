from django.contrib import admin
from .models import UserProfile, Menu, UserMenuOrder
from import_export import resources
from import_export.fields import Field
from import_export.widgets import DecimalWidget


class MenuAdmin(admin.ModelAdmin):
    list_display=['name', 'module', 'menu_type','url_name','icon_class']
    readonly_fields = ('date_created', 'date_updated', 'created_by', 'updated_by')

class UserMenuInline(admin.TabularInline):
    model = UserMenuOrder
    extra = 1


class UserProfileAdmin(admin.ModelAdmin):
    list_display=['user']
    inlines = [UserMenuInline]
    readonly_fields = ('date_created', 'date_updated', 'created_by', 'updated_by')


class MenuResource(resources.ModelResource):
    class Meta:
        model = Menu
        fields = export_order = ('name', 'menu_type', 'url_name', 'icon_class')


class UserProfileResource(resources.ModelResource):
    user = Field(column_name='User')
    about = Field(column_name='About')
    company = Field(column_name='Company')
    job = Field(column_name='Job')

    class Meta:
        model = UserProfile
        fields = ('user', 'about', 'company', 'job')
        export_order = ('user', 'about', 'company', 'job')

    def dehydrate_user(self, obj):
        return str(f"{obj.user:06}")

    def dehydrate_about(self, obj):
        return obj.about

    def dehydrate_company(self, obj):
        return obj.company

    def dehydrate_company(self, obj):
        return obj.company


admin.site.register(Menu,MenuAdmin)
admin.site.register(UserProfile,UserProfileAdmin)
 