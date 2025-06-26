from base.scaffolding import CrudManager

from .forms import DocHeaderForm
from .models import DocHeader
from .tables import DocHeaderTable
from .filters import DocHeaderFilter


class DocHeaderCrudManager(CrudManager):
    form_class = DocHeaderForm
    model = DocHeader
    module = 'document'
    prefix = 'docheader'
    table_class = DocHeaderTable
