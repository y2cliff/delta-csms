# from django.contrib import admin
from django.urls import path
from . import views
# from base.views import get_obj_list
# from scrum.models import Work
# from base.views import BaseView
# from .models import DailyWork
from . import scaffolding
from base.views import TemplateHomeView

from utils import navigate

app_name='project'


urlpatterns = [
	path('', TemplateHomeView.as_view(
		template_name = 'project/index.html', 
		module='project',
		page_name='Dashboard',
		page_title='Project Module',
		parent_menu=[['Project','project:home']]
	), name="home"),
	
	path('productivity/', views.get_productivity, name='productivity'),
	path('calendar/', views.calendar_view, name='calendar'),
	path('events-json/', views.events_json, name="events_json"),
    path('update-event/', views.update_event, name="update_event"),

]
urlpatterns += scaffolding.SiteCrudManager().get_url_patterns()
urlpatterns += scaffolding.BudgetItemCrudManager().get_url_patterns()
urlpatterns += scaffolding.ActivityCrudManager().get_url_patterns()
urlpatterns += scaffolding.CategoryCrudManager().get_url_patterns()
urlpatterns += scaffolding.TaskCrudManager().get_url_patterns()
urlpatterns += scaffolding.WorkCrudManager().get_url_patterns()
urlpatterns += scaffolding.UserWorkDateCrudManager().get_url_patterns()
urlpatterns += scaffolding.DailyWorkCrudManager().get_url_patterns()
urlpatterns += scaffolding.TaskChildCrudManager().get_url_patterns()
urlpatterns += scaffolding.BudgetItemChildCrudManager().get_url_patterns()
urlpatterns += scaffolding.ActivityChildCrudManager().get_url_patterns()
urlpatterns += scaffolding.DailyWorkChildCrudManager().get_url_patterns()

