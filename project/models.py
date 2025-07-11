from base.abstract import TemplateModel
from base.models import Department
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum, F
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
import datetime


class ProjDashboard(TemplateModel):
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='project_dashboard',
    )

    @property
    def get_productivity(self):
        s = UserWorkDate.objects.filter(user=self.user).aggregate(total_hours=Sum(
            F("regular_hrs") + F("ot_hrs")))["total_hours"] or 0
        w = DailyWork.objects.filter(workdate__user=self.user).aggregate(total_hours=Sum("work_hrs"))["total_hours"] or 0
        if s == 0:
            return 0
        return w/s * 100

    @property
    def get_efficiency(self):
        w = DailyWork.objects.filter(workdate__user=self.user).aggregate(total_hours=Sum("work_hrs"))["total_hours"] or 0
        b = DailyWork.objects.filter(workdate__user=self.user).aggregate(total_hours=Sum(
            F("quantity_pct") * F("work__benchmark_hrs")))["total_hours"] or 0
        if w == 0:
            return 0
        return b/w

    @property
    def get_proficiency(self):
        b = DailyWork.objects.filter(workdate__user=self.user).aggregate(total_hours=Sum(
            F("quantity_pct") * F("work__benchmark_hrs")))["total_hours"] or 0
        s = UserWorkDate.objects.filter(user=self.user).aggregate(total_hours=Sum("regular_hrs"))["total_hours"] or 0
        if s == 0:
            return 0
        return b/s

    @property
    def get_schedule(self):
        s = UserWorkDate.objects.filter(user=self.user).aggregate(total_hours=Sum("regular_hrs"))["total_hours"] or 0
        return s

    @property
    def get_overtime(self):
        e = UserWorkDate.objects.filter(user=self.user).aggregate(total_hours=Sum("ot_hrs"))["total_hours"] or 0
        return e
    
    @property
    def get_offduty(self):
        e = UserWorkDate.objects.filter(user=self.user).aggregate(total_hours=Sum("offduty_hrs"))["total_hours"] or 0
        return e

    @property
    def get_travel(self):
        e = UserWorkDate.objects.filter(user=self.user).aggregate(total_hours=Sum("travel_hrs"))["total_hours"] or 0
        return e
    
    @property
    def get_work(self):
        e = DailyWork.objects.filter(workdate__user=self.user).aggregate(total_hours=Sum("work_hrs"))["total_hours"] or 0
        return e
    
    @property
    def get_benchmark(self):
        e = DailyWork.objects.filter(workdate__user=self.user).aggregate(total_hours=Sum(
            F("quantity_pct") * F("work__benchmark_hrs") / 100))["total_hours"] or 0
        return e
    
    # @property
    # def get_travel(self):
    #     e = DailyWork.objects.filter(workdate__user=self.user, work__code__in=['W011f','W011g','W011k','W011h']
    #         ).aggregate(total_hours=Sum("work_hrs"))["total_hours"] or 0
    #     return e

    @property
    def get_leave(self):
        e = UserWorkDate.objects.filter(user=self.user
            ).aggregate(total_hours=Sum("regular_hrs"))["total_hours"] or 0
        return 0


class Site(TemplateModel):
    code = models.CharField(
        max_length=10, 
        unique=True, 
        error_messages={'unique': "Code has already been used."}
    )
    name = models.CharField(max_length=60, blank=True, null=True)

    class Meta:
        ordering = ["code"]
        permissions = (
            ('delete_foreign_site', _('Can delete foreign site')),
        )

    def __str__(self):
        return self.code + ' - ' + self.name

    def get_absolute_url(self):
        return reverse('project:site-detail',kwargs={'pk': self.id})


class ProjCategory(TemplateModel):
    code = models.CharField(
        max_length=10, 
        unique=True, 
        error_messages={'unique': "Code already exists."}
    )
    name = models.CharField(max_length=60, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Categories'
        permissions = (
            ('delete_foreign_category', _('Can delete foreign category')),
        )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('project:projcategory-detail',kwargs={'pk': self.id})


class BudgetItem(TemplateModel):
    # BUDGET_TYPE = (
    #     ('ADM','Administrative'),
    #     ('COM','Communications'),
    #     ('NET','Network'),
    #     ('SYS','System'),
    #     ('SEC','Security'),
    #     ('TECH','Technical')
    # )
    department = models.ForeignKey(Department, on_delete=models.PROTECT, blank=True, null=True, related_name='budget_items')
    code = models.CharField(
        max_length=10, 
        unique=True, 
        error_messages={'unique': "Code already exists."}
    )
    name = models.CharField(max_length=60, blank=True, null=True)
    # site = models.ForeignKey(Site, on_delete=models.PROTECT, blank=True, null=True, related_name='budget_items')
    # type = models.CharField(max_length=10, default="Admin", choices=BUDGET_TYPE)
    # amount = models.DecimalField(max_digits=18, decimal_places=2, default=0)

    class Meta:
        ordering = ["code"]
        verbose_name = 'Budget Item'
        permissions = (
            ('delete_foreign_budgetitem', _('Can delete foreign budget item')),
        )

    def __str__(self):
        return self.code + " - " + self.name

    def get_absolute_url(self):
        return reverse('project:budgetitem-detail',kwargs={'pk': self.id})


# STATUS
# Completed 
# Awaiting Appo
# Open
# Pending (Lacking )
# On-hold (Park)
# Cancelled

class Activity(TemplateModel):
    COLOR_CHOICES = [
        ('#3d3d3d', 'Black'),
        ('#4285f4', 'Blue'),
        ('#753800', 'Brown'),
        ('#34a853', 'Green'),
        ('#ea4335', 'Red'),
        ('#ffc107', 'Yellow'),
        ('#fd79a8', 'Pink'),
        ('#6f42c1', 'Purple')
    ]
    department = models.ForeignKey(Department, on_delete=models.PROTECT, blank=True, null=True, related_name='activities')
    code = models.CharField(
        max_length=10, 
        unique=True, 
        error_messages={'unique': "Code already exists."}
    )
    name = models.CharField(max_length=60, blank=True, null=True)
    site = models.ForeignKey('Site', on_delete=models.PROTECT, blank=True, null=True, related_name='activities')
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    leader = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null=True, related_name='lead_activities')
    followers = models.ManyToManyField(
        User,
        blank=True,
        symmetrical=False,
        related_name='activity_followers'
    )
    color = models.CharField(max_length=7, choices=COLOR_CHOICES, default='#007bff') 

    class Meta:
        ordering = ["-start_date"]
        verbose_name_plural = 'Activities'
        permissions = (
            ('delete_foreign_activity', _('Can delete foreign activity')),
        )

    @property
    def next_day_end(self):
        return self.end_date + datetime.timedelta(days=1)


    def __str__(self):
        return self.code + ' - ' + self.name

    def get_absolute_url(self):
        return reverse('project:activity-detail',kwargs={'pk': self.id})


class Task(TemplateModel):
    sequence = models.PositiveIntegerField(default=0)
    code = models.CharField(
        max_length=10
    )
    name = models.CharField(max_length=60, blank=True, null=True)
    activity = models.ForeignKey('Activity', on_delete=models.PROTECT, blank=True, null=True, related_name='tasks')
    budget_item = models.ForeignKey('BudgetItem', on_delete=models.PROTECT, blank=True, null=True, related_name='tasks')
    leader = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null=True, related_name='lead_tasks')
    followers = models.ManyToManyField(
        User,
        blank=True,
        symmetrical=False,
        related_name='task_followers'
    )

    class Meta:
        ordering = ["sequence"]
        permissions = (
            ('delete_foreign_task', _('Can delete foreign task')),
        )

    def __str__(self):
        return self.name

    def get_absolute_url(self): 
        return reverse('project:activity-detail',kwargs={'pk': self.activity.id})


class Work(TemplateModel):
    SKILL_LEVEL = (
        ('2','Expert'),
        ('1','Advanced'),
        ('0','Basic'),
        )
    YES_NO = (
        ('1','Yes'),
        ('0','No'),
        )
    code = models.CharField(max_length=15, blank=True, null=True)
    description = models.CharField(max_length=100, blank=True, null=True)
    parent_work = models.ForeignKey('self', on_delete=models.PROTECT, blank=True, null=True, related_name='children_work')
    min_hrs = models.DecimalField(max_digits=7, default="0", decimal_places=3, blank=True, null=True)
    max_hrs = models.DecimalField(max_digits=7, default="0", decimal_places=3, blank=True, null=True)
    benchmark_hrs = models.DecimalField(max_digits=7, default="0", decimal_places=3, blank=True, null=True)
    market_cost = models.DecimalField(max_digits=10, default="0", decimal_places=2, blank=True, null=True)
    skill_level = models.CharField(max_length=1, default="0", choices=SKILL_LEVEL)
    is_metered = models.CharField(max_length=1, default="0", choices=YES_NO)

    def __str__(self):
        return self.description

    class Meta:
        ordering = ["description"]
        permissions = (
            ('delete_foreign_work', _('Can delete foreign work')),
        )

    @property
    def min_target(self):
        return self.target_hrs * .75
    
    @property
    def max_target(self):
        return self.target_hrs * 1.25

    def get_absolute_url(self):
        return reverse('project:work-detail',kwargs={'pk': self.id})

    # def save(self):
    #     self.target_hrs = (self.min_hrs + self.max_hrs) / 2
    #     return super().save(self)

class UserWorkDate(TemplateModel):
    user = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null=True, related_name='workdate')
    workdate = models.DateField()
    regular_time = models.TimeField(default=datetime.time(0,0), blank=True, null=True )
    ot_time = models.TimeField(default=datetime.time(0,0), blank=True, null=True)
    offduty_time = models.TimeField(default=datetime.time(0,0), blank=True, null=True)
    travel_time = models.TimeField(default=datetime.time(0,0), blank=True, null=True)
    regular_hrs = models.DecimalField(max_digits=7, default="0", decimal_places=3, blank=True, null=True)
    ot_hrs = models.DecimalField(max_digits=7, default="0", decimal_places=3, blank=True, null=True)
    offduty_hrs = models.DecimalField(max_digits=7, default="0", decimal_places=3, blank=True, null=True)
    travel_hrs = models.DecimalField(max_digits=7, default="0", decimal_places=3, blank=True, null=True)

    def __str__(self):
        return self.user.username + " - " + self.workdate.strftime('%m/%d/%Y')

    @property
    def get_workdate_work_hrs(self):
        if self.workdate_dailywork.exists():
            a = self.workdate_dailywork.all()\
            .annotate(work_date=F("workdate")).values("work_date")\
            .annotate(total=Sum("work_hrs")).values("total")

            z = list(a[0].values())[0]
        else:
            z = 0
        return z

    class Meta:
        ordering = ["-workdate","user"]
        permissions = (
            ('delete_foreign_userworkdate', _('Can delete foreign userworkdate')),
        )

    def get_absolute_url(self):
        return reverse('project:userworkdate-detail',kwargs={'pk': self.id})

    def save(self, *args, **kwargs):
        if self.regular_time:
            self.regular_hrs = self.regular_time.hour + (self.regular_time.minute / 60)
        if self.ot_time:
            self.ot_hrs = self.ot_time.hour + (self.ot_time.minute / 60)
        if self.offduty_time:
            self.offduty_hrs = self.offduty_time.hour + (self.offduty_time.minute / 60)
        if self.travel_time:
            self.travel_hrs = self.travel_time.hour + (self.travel_time.minute / 60)
        super().save(*args, **kwargs)

    @property
    def get_sum_work(self):
        w = self.workdate_dailywork.aggregate(total_hours=Sum("work_hrs"))["total_hours"] or 0
        return w

    @property
    def get_productivity(self):
        sum_work = self.workdate_dailywork.aggregate(total_hours=Sum("work_hrs"))["total_hours"] or 0
        if self.regular_hrs == 0:
            return 0
        return sum_work / self.regular_hrs * 100

    @property
    def get_efficiency(self):
        sum_work = self.workdate_dailywork.aggregate(total_hours=Sum("work_hrs"))["total_hours"] or 0
        sum_benchmark = self.workdate_dailywork.aggregate(total_hours=Sum(F("quantity_pct") * F("work__benchmark_hrs")))["total_hours"] or 0
        if sum_work == 0:
            return 0
        return sum_benchmark / sum_work
        

    @property
    def get_proficiency(self):
        sum_benchmark = self.workdate_dailywork.aggregate(total_hours=Sum(F("quantity_pct") * F("work__benchmark_hrs")))["total_hours"] or 0
        if self.regular_hrs == 0:
            return 0
        return sum_benchmark / self.regular_hrs



class DailyWork(TemplateModel):
    SITUATION_LEVEL = (
        ('2','Difficult'),
        ('1','Normal'),
        ('0','Research'),
        )
    WORK_CLASS = (
        ('2','Overtime'),
        ('1','Regular'),
        ('0','Off-Duty'),
        )
    WORK_GROUP = (
        ('ADM','Admin'),
        ('SYS','System'),
        ('NET','Network'),
        ('TEC','Technical'),
        )
    workdate = models.ForeignKey(UserWorkDate, on_delete=models.PROTECT, blank=True, null=True, related_name='workdate_dailywork')
    work = models.ForeignKey(Work, on_delete=models.PROTECT, blank=True, null=True, related_name='work_dailywork')
    details = models.CharField(max_length=100, blank=True, null=True)
    work_time = models.TimeField(default=datetime.time(0,0), blank=True, null=True)
    work_hrs = models.DecimalField(max_digits=7, default="0", decimal_places=3, blank=True, null=True)
    situation = models.CharField(max_length=1, default="1", choices=SITUATION_LEVEL)
    work_class = models.CharField(max_length=1, default="1", choices=WORK_CLASS)
    work_group = models.CharField(max_length=3, default="ADM", choices=WORK_GROUP)
    quantity_pct = models.DecimalField(max_digits=7, default="0", decimal_places=0, blank=True, null=True)

    def __str__(self):
        return self.workdate.user.username + " - " + self.workdate.workdate.strftime('%m/%d/%Y') + " - " + self.work.description

    class Meta:
        ordering = ["-workdate"]
        permissions = (
            ('delete_foreign_dailywork', _('Can delete foreign dailywork')),
        )

    def get_absolute_url(self):
        return reverse('project:userworkdate-detail',kwargs={'pk': self.workdate.id})

    def save(self, *args, **kwargs):
        if self.work_time:
            self.work_hrs = self.work_time.hour + (self.work_time.minute / 60)
        super().save(*args, **kwargs)

    @property
    def quantity(self):
        return self.quantity_pct / 100

    # regular_hrs = self.workdate.regular_hrs 
    # sum_work_hrs = self.workdate.get_workdate_work_hrs
    # work_hrs = self.work_hrs    
    # qty_pct = self.quantity_pct
    # benchmark_hrs = self.work.benchmark_hrs
    

    @property
    def get_regular_hr_rated(self):
        # e = regular_hrs * (work_hrs / tot_hrs)
        # e = round((self.workdate.regular_hrs * (self.work_hrs / self.workdate.get_workdate_work_hrs)),2)
        e = 0
        if self.workdate.get_workdate_work_hrs != 0:
            e = self.workdate.regular_hrs * self.work_hrs / self.workdate.get_workdate_work_hrs
        return e

    @property
    def get_efficiency(self):
        # e = (qty_pct * benchmark_hrs) / work_hrs
        # e = round(((self.quantity_pct * self.work.benchmark_hrs) / self.work_hrs ),2)
        e = 0
        if self.work_hrs != 0:
            e = self.quantity_pct * self.work.benchmark_hrs / self.work_hrs
        return e

    @property
    def get_productivity(self):
        # e = sum_work_hrs / regular_hrs * 100 % 
        # e = round((self.workdate.get_workdate_work_hrs /  self.workdate.regular_hrs) * 100,2)
        e = 0
        if self.workdate.regular_hrs != 0:
            e = 100 * self.workdate.get_workdate_work_hrs / self.workdate.regular_hrs
        return e

    @property
    def get_proficiency(self):
        # e = efficiency * productivity
        e = 0
        if self.workdate.regular_hrs * self.work_hrs != 0:
            e = self.quantity_pct * self.work.benchmark_hrs * self.workdate.get_workdate_work_hrs / (self.workdate.regular_hrs * self.work_hrs)
        return e

