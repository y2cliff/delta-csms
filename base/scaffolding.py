
from django.urls import path
from . import views as core_views
from . import forms as core_forms
from . import models as core_models
from . import tables as core_tables
from . import filters as core_filters
from .admin import UserProfileResource, MenuResource


class CrudManager():
    model = core_models.UserProfile
    module = ''
    page_title = 'Menu'
    parent_menu = [["Home",'home']]
    page_name = 'Menu'
    model_resource = UserProfileResource
    extra_context = {}
    filterset_class = core_filters.UserProfileFilter     # FILTERS
    table_class = core_tables.UserProfileTable           # TABLES
    form_class = core_forms.UserProfileForm              # FORMS
    createview = core_views.TemplateCreateView           # VIEWS
    listview = core_views.TemplateListView
    detailview = core_views.TemplateDetailView
    updateview = core_views.TemplateUpdateView
    deleteview = core_views.TemplateDeleteView

    def get_url_patterns(self):
        url_patterns = [
            path(
                self.model._meta.model_name + '/',
                self.listview.as_view(
                    model=self.model,
                    module=self.module,
                    page_title=self.page_title + ' List',
                    parent_menu=self.parent_menu,
                    page_name='List',
                    model_resource=self.model_resource,
                    filterset_class=self.filterset_class,
                    table_class=self.table_class,
                    template_name='list.html',
                    context_object_name=self.model._meta.model_name + '_set',
                    extra_context=self.extra_context
                ),
                name=self.model._meta.model_name + '-list'
            ),
            path(
                self.model._meta.model_name + '/<int:pk>/',
                self.detailview.as_view(
                    model=self.model,
                    module=self.module,
                    page_title=self.page_title + ' Details',
                    parent_menu=self.parent_menu,
                    page_name='Detail',
                    template_name=self.model._meta.app_label+'/detail/'+self.model._meta.model_name+'.html',
                    permission_required=self.model._meta.app_label+'.view_'+self.model._meta.model_name,
                    extra_context=self.extra_context
                ),
                name=self.model._meta.model_name + '-detail'
            ),
            path(
                self.model._meta.model_name + '/create/',
                self.createview.as_view(
                    model=self.model,
                    module=self.module,
                    page_title='Create ' + self.page_title,
                    parent_menu=self.parent_menu,
                    page_name='Create',
                    form_class=self.form_class,
                    permission_required=self.model._meta.app_label + '.add_' + self.model._meta.model_name,
                    extra_context=self.extra_context
                ),
                name=self.model._meta.model_name + '-create'
            ),
            path(
                self.model._meta.model_name + '/<int:pk>/update/',
                self.updateview.as_view(
                    model=self.model,
                    module=self.module,
                    page_title='Update '+self.page_title,
                    parent_menu=self.parent_menu,
                    page_name='Update',
                    form_class=self.form_class,
                    permission_required=self.model._meta.app_label + '.change_' + self.model._meta.model_name,
                    extra_context=self.extra_context
                ),
                name=self.model._meta.model_name + '-update'
            ),
            path(
                self.model._meta.model_name + '/<int:pk>/delete/',
                self.deleteview.as_view(
                    extra_context=self.extra_context,
                    model=self.model,
                    module=self.module,
                    page_title=self.page_title,
                    parent_menu=self.parent_menu,
                    page_name=self.page_name,
                    # permission_required=self.model._meta.app_label + '.delete_' + self.model._meta.model_name,
                    url_path=self.model._meta.app_label + ':' + self.model._meta.model_name + '-list'
                ),
                name=self.model._meta.model_name + '-delete'
            )
        ]
        return url_patterns


class ChildCrudManager(CrudManager):
    # CHILD
    # child_prefix = ''
    # PARENT
    parent_model = core_models.UserProfile
    parent_prefix = ''
    # CHILD VIEWS
    createview = core_views.TemplateChildCreateView
    detailview = core_views.TemplateChildDetailView
    updateview = core_views.TemplateChildUpdateView
    deleteview = core_views.TemplateChildDeleteView

    def get_url_patterns(self):
        prefix = (
            self.parent_model._meta.model_name + '-' +
            self.model._meta.model_name
        )
        prefix_ = (
            self.parent_model._meta.model_name + '_' +
            self.model._meta.model_name
        )
        preurl = (
            self.parent_model._meta.model_name + '/<int:parent_id>/' +
            self.model._meta.model_name
        )
        url_path = (
            self.parent_model._meta.app_label + ':' +
            self.parent_model._meta.model_name + '-detail'
        )

        url_patterns = [
            # path(
            #     preurl + '/<int:id>/',
            #     self.detailview.as_view(
            #         extra_context=self.extra_context,
            #         model=self.model,
            #         parent_model=self.parent_model,
            #         permission_required=(
            #             self.model._meta.app_label + '.view_' + self.model._meta.model_name),
            #         template_name=self.model._meta.app_label + '/' + prefix_ + '_detail.html'
            #     ),
            #     name=self.parent_model._meta.model_name + '-detail'
            # ),
            path(
                preurl + '/create/',
                self.createview.as_view(
                    model=self.model,
                    module=self.module,
                    page_title='Create ' + self.page_title,
                    parent_menu=self.parent_menu,
                    page_name='Create',
                    form_class=self.form_class,
                    permission_required=self.model._meta.app_label + '.add_' + self.model._meta.model_name,
                    extra_context=self.extra_context,
                    parent_model=self.parent_model
                ),
                name=self.parent_model._meta.model_name + '-'+ self.parent_model._meta.model_name + '-create'
            ),
            # path(
            #     preurl + '/<int:id>/update/',
            #     self.updateview.as_view(
            #         extra_context=self.extra_context,
            #         form_class=self.form_class,
            #         model=self.model,
            #         module=self.module,
            #         page_title='Update ' + self.page_title,
            #         parent_menu=self.parent_menu,
            #         page_name=self.page_name,
            #         parent_model=self.parent_model,
            #         permission_required=(
            #             self.model._meta.app_label + '.change_' + self.model._meta.model_name)
            #     ),
            #     name=prefix + '-update'
            # ),
            # path(
            #     preurl + '/<int:id>/delete/',
            #     self.deleteview.as_view(
            #         extra_context=self.extra_context,
            #         model=self.model,
            #         module=self.module,
            #         page_title='Delete ' + self.page_title,
            #         parent_menu=self.parent_menu,
            #         page_name=self.page_name,
            #         parent_model=self.parent_model,
            #         permission_required=(
            #             self.model._meta.app_label + '.delete_' + self.model._meta.model_name),
            #         url_path=url_path
            #     ),
            #     name=self.parent_model._meta.model_name + '-delete'
            # )
        ]
        return url_patterns


class LineCrudManager():
    extra_context = {}
    model = core_models.UserProfile
    module = prefix = ''
    filterset_class = core_filters.UserProfileFilter    # FILTERS
    table_class = core_tables.UserProfileTable          # TABLES
    form_class = core_forms.UserProfileForm             # FORMS
    createview = core_views.TemplateCreateView          # VIEWS
    listview = core_views.TemplateListView
    detailview = core_views.TemplateDetailView
    updateview = core_views.TemplateUpdateView
    deleteview = core_views.TemplateDeleteView

    def get_url_patterns(self):
        url_patterns = [
            path(
                self.model._meta.model_name + '/',
                self.listview.as_view(
                    model=self.model,
                    module=self.module,
                    filterset_class=self.filterset_class,
                    table_class=self.table_class,
                    extra_context=self.extra_context
                ),
                name=self.model._meta.model_name + '-list'
            ),
            # path(
            #     self.prefix + '/<int:id>/',
            #     self.detailview.as_view(
            #         model=self.model,
            #         module=self.module,
            #         template_name=(
            #             self.module + '/' + self.prefix + '_detail.html'),
            #         permission_required=self.module + '.view_' + self.prefix,
            #         extra_context=self.extra_context
            #     ),
            #     name=self.prefix + '-detail'
            # ),
            path(
                self.model._meta.model_name + '/create/',
                self.createview.as_view(
                    model=self.model,
                    module=self.module,
                    form_class=self.form_class,
                    # permission_required=self.module + '.add_' + self.prefix,
                    extra_context=self.extra_context
                ),
                name=self.model._meta.model_name + '-create'
            ),
            # path(
            #     self.prefix + '/<int:id>/update/',
            #     self.updateview.as_view(
            #         model=self.model,
            #         form_class=self.form_class,
            #         permission_required=self.module + '.change_' + self.prefix,
            #         extra_context=self.extra_context
            #     ),
            #     name=self.prefix + '-update'
            # ),
            # path(
            #     self.prefix + '/<int:id>/delete/',
            #     self.deleteview.as_view(
            #         extra_context=self.extra_context,
            #         model=self.model,
            #         permission_required=self.module + '.delete_' + self.prefix,
            #         url_path=self.module + ':' + self.prefix + '-list'
            #     ),
            #     name=self.prefix + '-delete'
            # )
        ]
        return url_patterns


class MenuCrudManager(CrudManager):
    page_title = 'Menu'
    parent_menu = [['Menu','menu-list']]
    page_name = 'Menu'
    form_class = core_forms.MenuForm
    model = core_models.Menu
    table_class = core_tables.MenuTable
    filter_class = core_filters.MenuFilter
    module='base'
    model_resource = MenuResource


class UserProfileCrudManager(CrudManager):
    page_title = 'User Profile'
    parent_menu = [['Settings','userprofile-list']]
    page_name = 'User Profile'
    form_class = core_forms.UserProfileForm
    model = core_models.UserProfile
    table_class = core_tables.UserProfileTable
    filter_class = core_filters.UserProfileFilter
    module='base'


class UserMenuOrderCrudManager(ChildCrudManager):
    page_title = 'User menu'
    parent_menu = [['Settings','userprofile-list']]
    page_name = 'User menu'
    form_class = core_forms.UserMenuOrderForm
    model = core_models.UserMenuOrder
    # table_class = core_tables.UserProfileTable
    # filter_class = core_filters.UserProfileFilter
    module='base'

    parent_model = core_models.UserProfile
    # parent_prefix = 'userprofile'




