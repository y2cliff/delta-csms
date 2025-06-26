from datetime import datetime, timedelta
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.utils.formats import number_format
from django.urls import reverse
from django.shortcuts import render
from .models import Activity
from base.models import UserMenuOrder
import json


def get_productivity(request):
    timeframe = request.GET.get("timeframe", "this_month")

    data = {
        "this_month": request.user.project_dashboard.get_productivity if request.user.is_authenticated else 0,
        "this_year": request.user.project_dashboard.get_productivity if request.user.is_authenticated else 0,
        "all_time": request.user.project_dashboard.get_productivity if request.user.is_authenticated else 0
    }

    formatted_value = number_format(data.get(timeframe, 0), decimal_pos=2, use_l10n=True)
    return HttpResponse(f"<h6>{formatted_value}%</h6>")


def get_efficiency(request):
    timeframe = request.GET.get("timeframe", "this_month")

    data = {
        "this_month": request.user.project_dashboard.get_productivity if request.user.is_authenticated else 0,
        "this_year": request.user.project_dashboard.get_productivity if request.user.is_authenticated else 0,
        "all_time": request.user.project_dashboard.get_productivity if request.user.is_authenticated else 0
    }

    formatted_value = number_format(data.get(timeframe, 0), decimal_pos=2, use_l10n=True)
    return HttpResponse(f"<h6>{formatted_value}%</h6>")


def get_proficiency(request):
    timeframe = request.GET.get("timeframe", "this_month")

    data = {
        "this_month": request.user.project_dashboard.get_productivity if request.user.is_authenticated else 0,
        "this_year": request.user.project_dashboard.get_productivity if request.user.is_authenticated else 0,
        "all_time": request.user.project_dashboard.get_productivity if request.user.is_authenticated else 0
    }

    formatted_value = number_format(data.get(timeframe, 0), decimal_pos=2, use_l10n=True)
    return HttpResponse(f"<h6>{formatted_value}%</h6>")

def calendar_view(request):
    activities = Activity.objects.filter(Q(followers=request.user) | Q(leader=request.user)).distinct()
    context = {
        'activities': activities,
        'user_menus': UserMenuOrder.objects.my_module_menus(
            module= 'project', 
            user=request.user) or None,
        'module': 'project',
        'model':  'Activity',
        'page_name': 'Calendar',
        'page_title': 'Activity Calendar',
        'parent_menu': [['Project','project:home'], ['Activity','project:activity-list']]
    }
    return render(request, 'project/editable-calendar.html', context)


def events_json(request):
    user = request.user
    events = Activity.objects.filter(Q(followers=request.user) | Q(leader=request.user)).distinct()
    event_list = [{
        "id": event.id,
        "title": event.name,
        "start": event.start_date.strftime("%Y-%m-%d"),
        "end": event.next_day_end.strftime("%Y-%m-%d") if event.end_date else None,
        "url": reverse("project:activity-detail", kwargs={"pk": event.id}),
        "color": event.color,
        "editable": event.leader.username == user.username
    } for event in events]
    return JsonResponse(event_list, safe=False)


def update_event(request):
    if request.method == "POST":
        data = json.loads(request.body)

        # Convert timestamp to valid YYYY-MM-DD format
        start_date = datetime.strptime(data["start"], "%Y-%m-%dT%H:%M:%S.%fZ").date()
        end_date = datetime.strptime(data["end"], "%Y-%m-%dT%H:%M:%S.%fZ").date() if data.get("end") else None

        if start_date:
            start_date += timedelta(days=1)

        event = Activity.objects.get(id=data["id"])
        event.start_date = start_date
        event.end_date = end_date
        event.save()

        return JsonResponse({"status": "success"})
