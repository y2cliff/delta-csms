from django.urls import path
from .views import add_document, delete_document
from .scaffolding import DocHeaderCrudManager
from base.views import TemplateHomeView

app_name = 'document'

urlpatterns = [
    path('add-for/<app_label>/<model_name>/<int:pk>/',add_document,name="add"),
    path('delete/<int:document_pk>/', delete_document, name="delete"),
    path('', TemplateHomeView.as_view(template_name='document/document_home.html'),name='home'),
]

urlpatterns += DocHeaderCrudManager().get_url_patterns()
