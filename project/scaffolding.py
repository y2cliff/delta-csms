from base.scaffolding import CrudManager, ChildCrudManager
from base.views import TemplateChildCreateView, TemplateChildDeleteView
# from xystum import syscode
from .forms import SiteForm, BudgetItemForm, ActivityForm, TaskForm, CategoryForm, WorkForm, UserWorkDateForm, DailyWorkForm
from .models import Site, BudgetItem, Activity, Task, Category, Work, UserWorkDate, DailyWork
from .tables import SiteTable, BudgetItemTable, ActivityTable, TaskTable, CategoryTable, WorkTable, UserWorkDateTable, DailyWorkTable
from .filters import SiteFilter, BudgetItemFilter, ActivityFilter, TaskFilter, CategoryFilter, WorkFilter, UserWorkDateFilter, DailyWorkFilter
from .admin import SiteResource, BudgetItemResource, ActivityResource, TaskResource, CategoryResource, WorkResource


class SiteCrudManager(CrudManager):
    page_title = 'Site'
    parent_menu = [["Project",'project:home'],["Site",'project:site-list']]
    page_name = 'Site'
    form_class = SiteForm
    model = Site
    table_class = SiteTable
    module = 'project'
    model_resource = SiteResource
    

class BudgetItemCrudManager(CrudManager):
    page_title = 'Budget Item'
    parent_menu = [["Project",'project:home'],["Budget Item",'project:budgetitem-list']]
    page_name = 'List'
    form_class = BudgetItemForm
    model = BudgetItem
    table_class = BudgetItemTable
    module = 'project'
    model_resource = BudgetItemResource


class ActivityCrudManager(CrudManager):
    page_title = 'Activity'
    parent_menu = [["Project",'project:home'],["Activity",'project:activity-list']]
    page_name = 'List'
    form_class = ActivityForm
    model = Activity
    table_class = ActivityTable
    module = 'project'
    model_resource = ActivityResource


class CategoryCrudManager(CrudManager):
    page_title = 'Category'
    parent_menu = [["Project",'project:home'],["Category",'project:category-list']]
    page_name = 'List'
    form_class = CategoryForm
    model = Category
    table_class = CategoryTable
    module = 'project'
    model_resource = CategoryResource


class TaskCrudManager(CrudManager):
    page_title = 'Task'
    parent_menu = [["Project",'project:home'],["Task",'project:task-list']]
    page_name = 'List'
    form_class = TaskForm
    model = Task
    table_class = TaskTable
    module = 'project'
    model_resource = TaskResource


class WorkCrudManager(CrudManager):
    page_title = 'Work'
    parent_menu = [["Project",'project:home'],["Work",'project:work-list']]
    page_name = 'List'
    form_class = WorkForm
    model = Work
    table_class = WorkTable
    module = 'project'
    model_resource = WorkResource


class UserWorkDateCrudManager(CrudManager):
    page_title = 'Work Date'
    parent_menu = [["Project",'project:home'],["Work Date",'project:userworkdate-list']]
    page_name = 'List'
    form_class = UserWorkDateForm
    model = UserWorkDate
    table_class = UserWorkDateTable
    module = 'project'
    # model_resource = TaskResource


class DailyWorkCrudManager(CrudManager):
    page_title = 'DailyWork'
    parent_menu = [["Project",'project:home'],["Daily Work",'project:dailywork-list']]
    page_name = 'List'
    form_class = DailyWorkForm
    model = DailyWork
    table_class = DailyWorkTable
    module = 'project'
    # model_resource = TaskResource


class TaskChildCrudManager(ChildCrudManager):
    parent_model = Activity
    page_title = 'Task'
    parent_menu = [["Project",'project:home'], ["Task",'project:task-list']]
    page_name = 'List'
    form_class = TaskForm
    model = Task
    table_class = TaskTable
    module = 'project'
    model_resource = TaskResource


class BudgetItemChildCrudManager(ChildCrudManager):
    parent_model = Site
    page_title = 'Budget Item'
    parent_menu = [["Project",'project:home'],["Budget Item",'project:budgetitem-list']]
    page_name = 'List'
    form_class = BudgetItemForm
    model = BudgetItem
    table_class = BudgetItemTable
    module = 'project'
    model_resource = BudgetItemResource


class ActivityChildCrudManager(ChildCrudManager):
    parent_model = Site
    page_title = 'Activity'
    parent_menu = [["Project",'project:home'], ["Activity",'project:activity-list']]
    page_name = 'List'
    form_class = ActivityForm
    model = Activity
    table_class = ActivityTable
    module = 'project'
    model_resource = ActivityResource


class DailyWorkChildCrudManager(ChildCrudManager):
    parent_model = UserWorkDate
    page_title = 'Daily Work'
    parent_menu = [["Project",'project:home'], ["Daily Work",'project:dailywork-list']]
    page_name = 'List'
    form_class = DailyWorkForm
    model = DailyWork
    table_class = DailyWorkTable
    module = 'project'
    # model_resource = ActivityResource
