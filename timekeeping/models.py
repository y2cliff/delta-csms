from base.abstract import TemplateModel
from project.models import Work
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum, F
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
import datetime


class Dashboard(TemplateModel):
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='project_dashboard',
    )

    @property
    def get_productivity(self):
        timesheet = Timesheet.objects.filter(user=self.user).aggregate(total_hours=Sum(
            F("regular_hrs") + F("ot_hrs")))["total_hours"] or 0
        action = Action.objects.filter(workdate__user=self.user).aggregate(total_hours=Sum("work_hrs"))["total_hours"] or 0
        if timesheet == 0:
            return 0
        return action/timesheet * 100

    @property
    def get_efficiency(self):
        total_action = Action.objects.filter(workdate__user=self.user).aggregate(total_hours=Sum("work_hrs"))["total_hours"] or 0
        bench = Action.objects.filter(workdate__user=self.user).aggregate(total_hours=Sum(
            F("quantity_pct") * F("work__benchmark_hrs")))["total_hours"] or 0
        if total_action == 0:
            return 0
        return bench/total_action

    @property
    def get_proficiency(self):
        bench = Action.objects.filter(workdate__user=self.user).aggregate(total_hours=Sum(
            F("quantity_pct") * F("work__benchmark_hrs")))["total_hours"] or 0
        timesheet = Timesheet.objects.filter(user=self.user).aggregate(total_hours=Sum("regular_hrs"))["total_hours"] or 0
        if timesheet == 0:
            return 0
        return bench/timesheet

    @property
    def get_schedule(self):
        timesheet = Timesheet.objects.filter(user=self.user).aggregate(total_hours=Sum("regular_hrs"))["total_hours"] or 0
        return timesheet

    @property
    def get_overtime(self):
        timesheet = Timesheet.objects.filter(user=self.user).aggregate(total_hours=Sum("ot_hrs"))["total_hours"] or 0
        return timesheet
    
    @property
    def get_offduty(self):
        timesheet = Timesheet.objects.filter(user=self.user).aggregate(total_hours=Sum("offduty_hrs"))["total_hours"] or 0
        return timesheet

    @property
    def get_travel(self):
        timesheet = Timesheet.objects.filter(user=self.user).aggregate(total_hours=Sum("travel_hrs"))["total_hours"] or 0
        return timesheet
    
    @property
    def get_work(self):
        total_action_work = Action.objects.filter(workdate__user=self.user).aggregate(total_hours=Sum("work_hrs"))["total_hours"] or 0
        return total_action_work
    
    @property
    def get_benchmark(self):
        bench = Action.objects.filter(workdate__user=self.user).aggregate(total_hours=Sum(
            F("quantity_pct") * F("work__benchmark_hrs") / 100))["total_hours"] or 0
        return bench
    
    # @property
    # def get_travel(self):
    #     e = DailyWork.objects.filter(workdate__user=self.user, work__code__in=['W011f','W011g','W011k','W011h']
    #         ).aggregate(total_hours=Sum("work_hrs"))["total_hours"] or 0
    #     return e

    @property
    def get_leave(self):
        timesheet = Timesheet.objects.filter(user=self.user
            ).aggregate(total_hours=Sum("regular_hrs"))["total_hours"] or 0
        return 0


class TimeSheet(TemplateModel):
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
        if self.actions.exists():
            a = self.actions.all()\
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
        return reverse('timekeeping:userworkdate-detail',kwargs={'pk': self.id})

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
        w = self.actions.aggregate(total_hours=Sum("work_hrs"))["total_hours"] or 0
        return w

    @property
    def get_productivity(self):
        sum_work = self.actions.aggregate(total_hours=Sum("work_hrs"))["total_hours"] or 0
        if self.regular_hrs == 0:
            return 0
        return sum_work / self.regular_hrs * 100

    @property
    def get_efficiency(self):
        sum_work = self.actions.aggregate(total_hours=Sum("work_hrs"))["total_hours"] or 0
        sum_benchmark = self.actions.aggregate(total_hours=Sum(F("quantity_pct") * F("work__benchmark_hrs")))["total_hours"] or 0
        if sum_work == 0:
            return 0
        return sum_benchmark / sum_work
        

    @property
    def get_proficiency(self):
        sum_benchmark = self.actions.aggregate(total_hours=Sum(F("quantity_pct") * F("work__benchmark_hrs")))["total_hours"] or 0
        if self.regular_hrs == 0:
            return 0
        return sum_benchmark / self.regular_hrs



class Action(TemplateModel):
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
    timesheet = models.ForeignKey(TimeSheet, on_delete=models.PROTECT, blank=True, null=True, related_name='actions')
    work = models.ForeignKey(Work, on_delete=models.PROTECT, blank=True, null=True, related_name='action')
    details = models.CharField(max_length=100, blank=True, null=True)
    work_time = models.TimeField(default=datetime.time(0,0), blank=True, null=True)
    work_hrs = models.DecimalField(max_digits=7, default="0", decimal_places=3, blank=True, null=True)
    situation = models.CharField(max_length=1, default="1", choices=SITUATION_LEVEL)
    work_class = models.CharField(max_length=1, default="1", choices=WORK_CLASS)
    work_group = models.CharField(max_length=3, default="ADM", choices=WORK_GROUP)
    quantity_pct = models.DecimalField(max_digits=7, default="0", decimal_places=0, blank=True, null=True)

    def __str__(self):
        return self.timesheet.user.username + " - " + self.timesheet.workdate.strftime('%m/%d/%Y') + " - " + self.work.description

    class Meta:
        ordering = ["-timesheet"]
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
        if self.timesheet.get_workdate_work_hrs != 0:
            e = self.timesheet.regular_hrs * self.work_hrs / self.timesheet.get_workdate_work_hrs
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
        if self.timesheet.regular_hrs != 0:
            e = 100 * self.timesheet.get_workdate_work_hrs / self.timesheet.regular_hrs
        return e

    @property
    def get_proficiency(self):
        # e = efficiency * productivity
        e = 0
        if self.timesheet.regular_hrs * self.work_hrs != 0:
            e = self.quantity_pct * self.work.benchmark_hrs * self.timesheet.get_workdate_work_hrs / (self.timesheet.regular_hrs * self.work_hrs)
        return e

