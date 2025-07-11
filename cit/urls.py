from django.urls import path
from . import views
from . import scaffolding
from base.views import TemplateHomeView

from utils import navigate

app_name='cit'


urlpatterns = [
	path('', TemplateHomeView.as_view(
		template_name = 'cit/index.html', 
		module='cit',
		page_name='Dashboard',
		page_title='CIT Module',
		parent_menu=[['CIT','cit:home']]
	), name="home"),
	
	# path('productivity/', views.get_productivity, name='productivity'),
	# path('calendar/', views.calendar_view, name='calendar'),
	# path('events-json/', views.events_json, name="events_json"),
    # path('update-event/', views.update_event, name="update_event"),

]
urlpatterns += scaffolding.ManufacturerCrudManager().get_url_patterns()
urlpatterns += scaffolding.RadioCrudManager().get_url_patterns()
urlpatterns += scaffolding.RadioLicenseCrudManager().get_url_patterns()
