import django_tables2 as tables
from base.tables import ATTRS
from .models import DocHeader


class DocHeaderTable(tables.Table):
    name = tables.Column(linkify=True)

    class Meta:
        model = DocHeader
        attrs = ATTRS
        fields = ('name','groups')
        sequence = ('name','groups')
