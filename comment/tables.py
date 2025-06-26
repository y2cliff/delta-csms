import django_tables2 as tables
from base.tables import ATTRS
from .models import Post


class PostTable(tables.Table):
    created_by = tables.Column(linkify=True)

    class Meta:
        model = Post
        attrs = ATTRS
        fields = ('created_by','message')
        sequence = ('created_by','message')
