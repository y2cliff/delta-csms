import django_tables2 as tables
from .models import UserProfile, Menu
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


class UserProfileTable(tables.Table):
    user = tables.Column(linkify=True)
    full_name = tables.Column(accessor='get_full_name', verbose_name='Full Name')

    class Meta:
        model = UserProfile
        attrs = ATTRS
        fields = sequence = ('user', 'user__email', 'company', 'full_name', 'job')


class MenuTable(tables.Table):
    name = tables.Column(linkify=True)
    icon_class = tables.TemplateColumn(
        template_code=
            """
            <i class= "bi bi-{{record.icon_class}}"></i> [ {{record.icon_class}} ]
            """
        )

    class Meta:
        model = Menu
        attrs = ATTRS
        fields = sequence = ('name', 'module', 'menu_type', 'url_name', 'icon_class')

    def render_module(self, value):
        return value.title()
