from django.urls import path
from . import scaffolding
from base.views import TemplateHomeView

app_name='inventory'


urlpatterns = [
	path('', TemplateHomeView.as_view(
		template_name = 'inventory/index.html', 
		module='inventory',
		page_name='Dashboard',
		page_title='Inventory Module',
		parent_menu=[['Inventory','inventory:home']]
	), name="home"),

]
urlpatterns += scaffolding.InvCategoryCrudManager().get_url_patterns()