from django import forms
from django.core.exceptions import ValidationError
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.contrib.auth.models import User
from django.utils import timezone
from django.shortcuts import reverse

from django_select2.forms import Select2Widget, ModelSelect2Widget

from crispy_forms.layout import Field, Row, Column, HTML
from crispy_bootstrap5.bootstrap5 import FloatingField

from base.forms import Helper, SELECTFILTER_CSS, ClearableSelect2Widget
from . import models
from django_currentuser.middleware import get_current_user
import datetime

from django.utils.safestring import mark_safe


class UserSelect2Widget(ClearableSelect2Widget):
    queryset = User.objects.all()


class SiteForm(forms.ModelForm):

    class Meta:
        model = models.Site
        fields = ['code','name']

    class Media:
        css = SELECTFILTER_CSS
        js = ['/admin/jsi18n',]

    def __init__(self, *args, **kwargs):
        self.helper = Helper()
        self.helper.field_layout(
            Row(
            Column(FloatingField('code'),css_class="col-lg-2"),   
            Column(FloatingField('name'),css_class="col-lg-10")
            )
        )
        super(SiteForm, self).__init__(*args, **kwargs)


    def clean_code(self):
        code = self.cleaned_data['code']
        if not self.instance and models.Site.objects.filter(code=code).exists():
            raise forms.ValidationError(f"Code already exists.")
        return code

    def get_cancel_url(self):
        return reverse('project:site-list')


class BudgetItemForm(forms.ModelForm):

    class Meta:
        model = models.BudgetItem
        fields = ['code','name', 'site', 'type','amount']
        widgets = {
            'site': ClearableSelect2Widget(attrs={"data-placeholder": "select an option"}),
            'type': ClearableSelect2Widget(attrs={"data-placeholder": "select an option"})
        }

    class Media:
        css = SELECTFILTER_CSS
        js = ['/admin/jsi18n',]

    def __init__(self, *args, **kwargs):
        self.helper = Helper()
        self.helper.field_layout(
            Row(
                Column(FloatingField('code'),css_class="col-lg-2"),
                Column(FloatingField('name'),css_class="col-lg-10")
            ),
            Row(
                Column(FloatingField('site'),css_class="col-lg-5"),
                Column(FloatingField('type'),css_class="col-lg-4"),
                Column(FloatingField('amount'),css_class="col-lg-3")
            )
        )
        parent_ = kwargs.pop('parent_id', '')
        super(BudgetItemForm, self).__init__(*args, **kwargs)
        if parent_:
            self.initial['site'] = models.Site.objects.get(id=parent_)
            self.fields['site'].queryset = Site.objects.filter(id=parent_)
            self.fields['site'].required = True

    def clean_code(self):
        code = self.cleaned_data['code']
        if not self.instance and models.BudgetItem.objects.filter(code=code).exists():
            raise ValidationError(f"Code already exists.")
        return code

    def get_cancel_url(self):
        return reverse('project:budgetitem-list')


class ProjCategoryForm(forms.ModelForm):

    class Meta:
        model = models.ProjCategory
        fields = ['code','name']

    class Media:
        css = SELECTFILTER_CSS
        js = ['/admin/jsi18n',]

    def __init__(self, *args, **kwargs):
        self.helper = Helper()
        self.helper.field_layout(
            Row(
                Column(FloatingField('code'),css_class="col-lg-2"),
                Column(FloatingField('name'),css_class="col-lg-10")
            )
        )
        super(ProjCategoryForm, self).__init__(*args, **kwargs)

    def clean_code(self):
        code = self.cleaned_data['code']
        if not self.instance and models.Category.objects.filter(code=code).exists():
            raise ValidationError(f"Code already exists.")
        return code

    # def get_cancel_url(self):
    #     return reverse('project:budgetitem-list')


class UserFullNameChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.get_full_name() or obj.username


class ActivityForm(forms.ModelForm):
    start_date = forms.DateField(
        required=False,
        label='Start Date',
        widget=forms.TextInput(attrs={'type': 'date'}),
        initial=timezone.now().date
    )
    end_date = forms.DateField(
        required=False,
        label='End Date',
        widget=forms.TextInput(attrs={'type': 'date'}),
        initial=timezone.now().date
    )
    leader = UserFullNameChoiceField(
        queryset=User.objects.all(),
        required=True,
        widget=ClearableSelect2Widget(attrs={"data-placeholder": "select an option"})
    )
    followers = forms.ModelMultipleChoiceField(
        queryset = User.objects.all(),
        required=False,
        widget=FilteredSelectMultiple("Followers", is_stacked=False)
    )

    class Media:
        css = SELECTFILTER_CSS
        js = ['/admin/jsi18n',]

    class Meta:
        model = models.Activity
        fields = ['code','name', 'site', 'start_date', 'end_date', 'leader','followers', 'color']
        widgets = {
            'site': ClearableSelect2Widget(attrs={"data-placeholder": "select an option"}),
            'color': ClearableSelect2Widget(attrs={"data-placeholder": "select an option"})
        }

    def __init__(self, *args, **kwargs):
        self.helper = Helper()
        self.helper.field_layout(
            Row(
                Column(FloatingField('code'),css_class="col-lg-3"),
                Column(FloatingField('start_date'),css_class="col-lg-3"),
                Column(FloatingField('end_date'),css_class="col-lg-3"),
                Column(FloatingField('color'),css_class="col-lg-3")
            ),
            Row(
                Column(FloatingField('name'),css_class="col-lg-12")
            ),
            Row(
                Column(FloatingField('site'),css_class="col-lg-6"),
                Column(FloatingField('leader'),css_class="col-lg-6")
            ),
            Row(
                Column(FloatingField('followers'),css_class="col-12")
            )
        )
        parent_ = kwargs.pop('parent_id', '')
        super(ActivityForm, self).__init__(*args, **kwargs)
        if parent_:
            self.initial['site'] = models.Site.objects.get(id=parent_)
            self.fields['site'].queryset = models.Site.objects.filter(id=parent_)
            self.fields['site'].required = True
        self.fields["followers"].label_from_instance = lambda obj: obj.get_full_name() or obj.username

    def clean_code(self):
        code = self.cleaned_data['code']
        if not self.instance and models.Activity.objects.filter(code=code).exists():
            raise ValidationError(f"Code already exists.")
        return code

    def get_cancel_url(self):
        return reverse('project:activity-list')


class TaskForm(forms.ModelForm):
    leader = UserFullNameChoiceField(
        queryset=User.objects.all(),
        required=True,
        widget=ClearableSelect2Widget(attrs={"data-placeholder": "select an option"})
    )
    followers = forms.ModelMultipleChoiceField(
        queryset = User.objects.all(),
        required=False,
        widget=FilteredSelectMultiple("Followers", is_stacked=False)
        )

    class Meta:
        model = models.Task
        fields = ['activity','sequence', 'code', 'name','leader','budget_item','followers']
        widgets = {
            'activity': ClearableSelect2Widget(attrs={"data-placeholder": "select an option"}),
            'budget_item': ClearableSelect2Widget(attrs={"data-placeholder": "select an option"})
        }

    class Media:
        css = SELECTFILTER_CSS
        js = ['/admin/jsi18n',]

    def __init__(self, *args, **kwargs):
        self.helper = Helper()
        self.helper.field_layout(
            Row(
                Column(FloatingField('activity'),css_class="col-xl-10"),
                Column(FloatingField('sequence'),css_class="col-xl-2")
            ),
            Row(
                Column(FloatingField('name'),css_class="col-xl-10"),
                Column(FloatingField('code'),css_class="col-xl-2")
            ),
            Row(
                Column(FloatingField('leader'),css_class="col-lg-6"),
                Column(FloatingField('budget_item'),css_class="col-lg-6")
            ),
            Row(
                Column(FloatingField('followers'),css_class="col-lg-12")
            )

        )
        parent_ = kwargs.pop('parent_id', '')
        super(TaskForm, self).__init__(*args, **kwargs)
        if parent_:
            self.initial['activity'] = models.Activity.objects.get(id=parent_)
            self.fields['activity'].queryset = models.Activity.objects.filter(id=parent_)
            self.fields['activity'].required = True
        self.fields["followers"].label_from_instance = lambda obj: obj.get_full_name() or obj.username

    def clean_code(self):
        code = self.cleaned_data['code']
        if not self.instance and models.Task.objects.filter(code=code).exists():
            raise forms.ValidationError(f"Code already exists.")
        return code

    def get_cancel_url(self):
        return reverse('project:task-list')


class WorkForm(forms.ModelForm):

    class Meta:
        model = models.Work
        fields = ['code','description', 'parent_work', 'min_hrs', 'max_hrs', 'benchmark_hrs', 'market_cost', 'skill_level', 'is_metered']
        widgets = {
            'parent_work': ClearableSelect2Widget(attrs={"data-placeholder": "select an option"})
        }

    class Media:
        css = SELECTFILTER_CSS
        js = ['/admin/jsi18n',]

    def __init__(self, *args, **kwargs):
        self.helper = Helper()
        self.helper.field_layout(
            Row(
                Column(FloatingField('code'),css_class="col-lg-2"),
                Column(FloatingField('description'),css_class="col-lg-10")
            ),
            Row(
                Column(FloatingField('parent_work'),css_class="col-lg-8"),
                Column(FloatingField('skill_level'),css_class="col-lg-4")
            ),
            Row(
                Column(FloatingField('benchmark_hrs'),css_class="col-lg-3"),
                Column(FloatingField('min_hrs'),css_class="col-lg-2"),
                Column(FloatingField('max_hrs'),css_class="col-lg-2"),
                Column(FloatingField('market_cost'),css_class="col-lg-3"),
                Column(FloatingField('is_metered'),css_class="col-lg-2")
            )
        )
        super(WorkForm, self).__init__(*args, **kwargs)

    def clean_code(self):
        code = self.cleaned_data['code']
        if not self.instance and models.Work.objects.filter(code=code).exists():
            raise ValidationError(f"Code already exists.")
        return code

    def get_cancel_url(self):
        return reverse('project:work-list')


class UserWorkDateForm(forms.ModelForm):
    workdate = forms.DateField(
        required=False,
        label='Work Date',
        widget=forms.TextInput(attrs={'type': 'date'}),
        initial=timezone.now().date
    )
    regular_time = forms.TimeField(
        required=False,
        label="Regular Time (HH:MM)",
        widget=forms.widgets.TimeInput(format='%H:%M'),
        initial=datetime.time(0,0)
    )
    ot_time = forms.TimeField(
        required=False,
        label="OT Time (HH:MM)",
        widget=forms.widgets.TimeInput(format='%H:%M'),
        initial=datetime.time(0,0)
    )
    offduty_time = forms.TimeField(
        required=False,
        label="Off Duty Time (HH:MM)",
        widget=forms.widgets.TimeInput(format='%H:%M'),
        initial=datetime.time(0,0)
    )
    travel_time = forms.TimeField(
        required=False,
        label="Travel Time (HH:MM)",
        widget=forms.widgets.TimeInput(format='%H:%M'),
        initial=datetime.time(0,0)
    )

    class Meta:
        model = models.UserWorkDate
        fields = ['user','workdate','regular_time','ot_time','offduty_time', 'travel_time']

    class Media:
        css = SELECTFILTER_CSS
        js = ['/admin/jsi18n',]

    def __init__(self, *args, **kwargs):
        self.helper = Helper()
        self.helper.field_layout(
            Row(
                Column(FloatingField('user'),css_class="col-lg-3"),
                Column(FloatingField('workdate'),css_class="col-lg-9")
            ),
            Row(
                Column(FloatingField('regular_time'),css_class="col-lg-3"),
                Column(FloatingField('ot_time'),css_class="col-lg-3"),
                Column(FloatingField('offduty_time'),css_class="col-lg-3"),
                Column(FloatingField('travel_time'),css_class="col-lg-3")
            )
        )
        super(UserWorkDateForm, self).__init__(*args, **kwargs)
        self.initial['user'] = get_current_user()


    def get_cancel_url(self):
        return reverse('project:userworkdate-list')


class DailyWorkForm(forms.ModelForm):
    work_time = forms.TimeField(
        required=False,
        label="Work Time (HH:MM)",
        widget=forms.widgets.TimeInput(format='%H:%M'),
        initial=datetime.time(0,0)
    )
   
    class Meta:
        model = models.DailyWork
        fields = ['workdate','work','details','work_time','situation','work_class','work_group','quantity_pct']
        widgets = {
            'work': ClearableSelect2Widget(attrs={"data-placeholder": "select an option"})
        }

    class Media:
        css = SELECTFILTER_CSS
        js = ['/admin/jsi18n',]

    def __init__(self, *args, **kwargs):
        self.helper = Helper()
        self.helper.field_layout(
            Row(
                Column(FloatingField('workdate'),css_class="col-lg-3"),
                Column(FloatingField('work'),css_class="col-lg-9")
            ),
            Row(
                Column(FloatingField('quantity_pct', wrapper_class='percentage-field'),css_class="col-lg-2"),
                Column(FloatingField('details'),css_class="col-lg-10")
            ),
            Row(
                Column(FloatingField('work_time'),css_class="col-lg-3"),
                Column(FloatingField('situation'),css_class="col-lg-3"),
                Column(FloatingField('work_class'),css_class="col-lg-3"),
                Column(FloatingField('work_group'),css_class="col-lg-3")

            )
        )
        parent_ = kwargs.pop('parent_id', '')        
        super(DailyWorkForm, self).__init__(*args, **kwargs)
        if parent_:
            self.initial['workdate'] = models.UserWorkDate.objects.get(id=parent_)
            self.fields['workdate'].queryset = UserWorkDate.objects.filter(id=parent_)
            self.fields['workdate'].required = True


    def get_cancel_url(self):
        return reverse('project:dailywork-list')

