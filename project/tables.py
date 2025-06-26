import django_tables2 as tables
from django.contrib.humanize.templatetags.humanize import intcomma
from .models import Site, BudgetItem, Activity, Task, Category, Work, UserWorkDate, DailyWork
from base.tables import ATTRS
from django import forms


class SiteTable(tables.Table):
    code = tables.Column(linkify=True)

    class Meta:
        model = Site
        attrs = ATTRS
        fields = sequence = ('code', 'name', 'is_active', 'date_created', 'date_updated')

    def render_is_active(self, value):
        if value:
            return 'Active'
        return 'Inactive'


class BudgetItemTable(tables.Table):
    code = tables.Column(linkify=True)
    amount = tables.Column()

    class Meta:
        model = BudgetItem
        attrs = ATTRS
        fields = sequence = ('code', 'name', 'site', 'type', 'amount')

    def render_amount(self, value):
        return intcomma(value)


class ActivityTable(tables.Table):
    name = tables.Column(linkify=True)
    site = tables.Column(accessor='site.code', verbose_name="Site")
    action = tables.TemplateColumn(template_code=
        '''
        <button id="follow-button-{{ record.id }}" class="btn btn-outline-info btn-sm" data-object-id="{{ record.id }}" data-app-name="project" data-model-name="activity">
            {% if request.user in record.followers.all %}
                <i class="bi bi-person-dash-fill"></i> Unfollow
            {% else %}
                <i class="bi bi-person-plus-fill"></i> Follow
            {% endif %}
        </button>
        '''
        )

    class Meta:
        model = Activity
        attrs = ATTRS
        fields = sequence = ('name', 'site', 'start_date', 'end_date','leader', 'action')


class CategoryTable(tables.Table):
    code = tables.Column(linkify=True)

    class Meta:
        model = Category
        attrs = ATTRS
        fields = sequence = ('code', 'name')

    def render_amount(self, value):
        return intcomma(value)


class TaskTable(tables.Table):
    activity = tables.Column(linkify=True)

    class Meta:
        model = Task
        attrs = ATTRS
        fields = sequence = ('activity', 'name', 'sequence', 'budget_item', 'leader')


class WorkTable(tables.Table):
    code = tables.Column(linkify=True)

    class Meta:
        model = Work
        attrs = ATTRS
        fields = sequence = ('code','description', 'benchmark_hrs', 'market_cost', 'skill_level', 'is_metered')


class UserWorkDateTable(tables.Table):
    workdate = tables.Column(linkify=True)
    f_regular_time = tables.Column(
        attrs={"td":{"style": "text-align: center;"}},
        accessor='regular_time', 
        verbose_name="Regular Time")
    f_ot_time = tables.Column(
        attrs={"td":{"style": "text-align: center;"}},
        accessor='ot_time', 
        verbose_name="OT Time")
    f_travel_time = tables.Column(
        attrs={"td":{"style": "text-align: center;"}},
        accessor='travel_time', 
        verbose_name="Travel Time")
    f_offduty_time = tables.Column(
        attrs={"td":{"style": "text-align: center;"}},
        accessor='offduty_time', 
        verbose_name="Off Duty Time")

    def render_f_regular_time(self, value):
        return value.strftime("%H:%M")

    def render_f_ot_time(self, value):
        return value.strftime("%H:%M")

    def render_f_travel_time(self, value):
        return value.strftime("%H:%M")

    def render_f_offduty_time(self, value):
        return value.strftime("%H:%M")

    class Meta:
        model = UserWorkDate
        attrs = ATTRS
        fields = sequence = ('workdate','user','f_regular_time', 'f_ot_time', 'f_travel_time', 'f_offduty_time')


class DailyWorkTable(tables.Table):
    details = tables.Column(linkify=True)

    class Meta:
        model = DailyWork
        attrs = ATTRS
        fields = sequence = ('workdate','work','details','work_hrs','situation','work_class','work_group','quantity_pct')
