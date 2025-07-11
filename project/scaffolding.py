from base.scaffolding import CrudManager, ChildCrudManager
from base.views import TemplateChildCreateView, TemplateChildDeleteView
# from xystum import syscode
from . import forms
from . import models
from . import tables
from . import filters
from . import admin


class SiteCrudManager(CrudManager):
    page_title = 'Site'
    parent_menu = [["Project",'project:home'],["Site",'project:site-list']]
    page_name = 'Site'
    form_class = forms.SiteForm
    model = models.Site
    table_class = tables.SiteTable
    filterset_class = filters.SiteFilter
    module = 'project'
    model_resource = admin.SiteResource
    
    
class BudgetItemCrudManager(CrudManager):
    page_title = 'Budget Item'
    parent_menu = [["Project",'project:home'],["Budget Item",'project:budgetitem-list']]
    page_name = 'List'
    form_class = forms.BudgetItemForm
    model = models.BudgetItem
    table_class = tables.BudgetItemTable
    filterset_class = filters.BudgetItemFilter
    module = 'project'
    model_resource = admin.BudgetItemResource
    

class ActivityCrudManager(CrudManager):
    page_title = 'Activity'
    parent_menu = [["Project",'project:home'],["Activity",'project:activity-list']]
    page_name = 'List'
    form_class = forms.ActivityForm
    model = models.Activity
    table_class = tables.ActivityTable
    filterset_class = filters.ActivityFilter
    module = 'project'
    model_resource = admin.ActivityResource
    

class ProjCategoryCrudManager(CrudManager):
    page_title = 'Project Category'
    parent_menu = [["Project",'project:home'],["Category",'project:category-list']]
    page_name = 'List'
    form_class = forms.ProjCategoryForm
    model = models.ProjCategory
    table_class = tables.ProjCategoryTable
    filterset_class = filters.ProjCategoryFilter
    module = 'project'
    model_resource = admin.ProjCategoryResource
    

class TaskCrudManager(CrudManager):
    page_title = 'Task'
    parent_menu = [["Project",'project:home'],["Task",'project:task-list']]
    page_name = 'List'
    form_class = forms.TaskForm
    model = models.Task
    table_class = tables.TaskTable
    filterset_class = filters.TaskFilter
    module = 'project'
    model_resource = admin.TaskResource
    

class WorkCrudManager(CrudManager):
    page_title = 'Work'
    parent_menu = [["Project",'project:home'],["Work",'project:work-list']]
    page_name = 'List'
    form_class = forms.WorkForm
    model = models.Work
    table_class = tables.WorkTable
    filterset_class = filters.WorkFilter
    module = 'project'
    model_resource = admin.WorkResource


class UserWorkDateCrudManager(CrudManager):
    page_title = 'Work Date'
    parent_menu = [["Project",'project:home'],["Work Date",'project:userworkdate-list']]
    page_name = 'List'
    form_class = forms.UserWorkDateForm
    model = models.UserWorkDate
    table_class = tables.UserWorkDateTable
    filterset_class = filters.UserWorkDateFilter
    module = 'project'
    # model_resource = TaskResource


class DailyWorkCrudManager(CrudManager):
    page_title = 'DailyWork'
    parent_menu = [["Project",'project:home'],["Daily Work",'project:dailywork-list']]
    page_name = 'List'
    form_class = forms.DailyWorkForm
    model = models.DailyWork
    table_class = tables.DailyWorkTable
    filterset_class = filters.DailyWorkFilter
    module = 'project'
    # model_resource = TaskResource


class TaskChildCrudManager(ChildCrudManager):
    parent_model = models.Activity
    page_title = 'Task'
    parent_menu = [["Project",'project:home'], ["Task",'project:task-list']]
    page_name = 'List'
    form_class = forms.TaskForm
    model = models.Task
    table_class = tables.TaskTable
    module = 'project'
    model_resource = admin.TaskResource


class BudgetItemChildCrudManager(ChildCrudManager):
    parent_model = models.Site
    page_title = 'Budget Item'
    parent_menu = [["Project",'project:home'],["Budget Item",'project:budgetitem-list']]
    page_name = 'List'
    form_class = forms.BudgetItemForm
    model = models.BudgetItem
    table_class = tables.BudgetItemTable
    module = 'project'
    model_resource = admin.BudgetItemResource


class ActivityChildCrudManager(ChildCrudManager):
    parent_model = models.Site
    page_title = 'Activity'
    parent_menu = [["Project",'project:home'], ["Activity",'project:activity-list']]
    page_name = 'List'
    form_class = forms.ActivityForm
    model = models.Activity
    table_class = tables.ActivityTable
    module = 'project'
    model_resource = admin.ActivityResource


class DailyWorkChildCrudManager(ChildCrudManager):
    parent_model = models.UserWorkDate
    page_title = 'Daily Work'
    parent_menu = [["Project",'project:home'], ["Daily Work",'project:dailywork-list']]
    page_name = 'List'
    form_class = forms.DailyWorkForm
    model = models.DailyWork
    table_class = tables.DailyWorkTable
    module = 'project'
    # model_resource = ActivityResource
