import django_tables2 as tables
from .models import InvCategory
from base.tables import ATTRS


class InvCategoryTable(tables.Table):
    code = tables.Column(linkify=True)

    class Meta:
        model = InvCategory
        attrs = ATTRS
        fields = sequence = ('code', 'name', 'description', 'date_created', 'date_updated')

    def render_is_active(self, value):
        if value:
            return 'Active'
        return 'Inactive'
