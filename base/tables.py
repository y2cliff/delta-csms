import django_tables2 as tables
from .models import UserProfile, GroupProfile, Menu, Department
from django.contrib.auth.models import User


ATTRS = {
    'class': 'table datatable table-striped w-100 d-block d-md-table',
    'id': 'dataTable',
    'thead': {
        'class': 'table-primary',
    },
    'th': {
        '_ordering': {
            'orderable': 'sortable',  # Instead of `orderable`
            'ascending': 'ascend',   # Instead of `asc`
            'descending': 'descend'  # Instead of `desc`
        },
    }
}

class TemplateTable(tables.Table):
    is_active = tables.Column(visible=False)
    id = tables.Column(visible=False)
    created_by = tables.Column(visible=False)
    date_created = tables.DateTimeColumn(format='Y-m-d H:i:s', visible=False)
    updated_by = tables.Column(visible=False)
    date_updated = tables.DateTimeColumn(format='Y-m-d H:i:s', visible=False)

class UserProfileTable(TemplateTable):
    user = tables.Column(linkify=True, verbose_name='User Name')
    full_name = tables.Column(accessor='get_full_name', verbose_name='Full Name')
    action = tables.TemplateColumn(exclude_from_export=True, template_code=
        '''
        <a href="{% url 'user-userprofile-update' record.user.id record.user.id %}" class="btn btn-outline-primary btn-sm"> 
        <i class="bi bi-pencil"></i> Edit</a>
        '''
        )

    class Meta:
        model = UserProfile
        attrs = ATTRS
        fields = sequence = ('user', 'user__email', 'full_name', 'action')

class GroupProfileTable(TemplateTable):
    group = tables.Column(linkify=True)
    action = tables.TemplateColumn(exclude_from_export=True, template_code=
        '''
        <a href="{% url 'group-groupprofile-update' record.group.id record.group.id %}" class="btn btn-outline-primary btn-sm"> 
        <i class="bi bi-pencil"></i> Edit</a>
        '''
        )

    class Meta:
        model = GroupProfile
        attrs = ATTRS
        fields = sequence = ('group', 'name')

class MenuTable(TemplateTable):
    code = tables.Column(linkify=True)
    icon_class = tables.TemplateColumn(
        template_code=
            """
            <i class= "bi bi-{{record.icon_class}}"></i> [ {{record.icon_class}} ]
            """
        )

    class Meta:
        model = Menu
        attrs = ATTRS
        fields = sequence = ('code','name', 'module', 'menu_type', 'url_name', 'icon_class')

    def render_module(self, value):
        return value.title()

class DepartmentTable(TemplateTable):
    code = tables.Column(linkify=True)

    class Meta:
        model = Department
        attrs = ATTRS
        fields = sequence = ('code', 'name')