from django.shortcuts import redirect
from django.apps import apps
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse


def next_record_view(request, app_name, model_name, current_id):
    ModelClass = apps.get_model(app_name, model_name)
    next_record = ModelClass.objects.filter(id__gt=current_id).order_by('id').first()
    detail_view_name = app_name +':'+ ModelClass._meta.model_name +'-detail'

    if next_record:
        return redirect(detail_view_name, pk=next_record.pk)

    return redirect(detail_view_name, pk=current_id)  # Stay on the same record if none found


def previous_record_view(request, app_name, model_name, current_id):
    ModelClass = apps.get_model(app_name, model_name)
    previous_record = ModelClass.objects.filter(id__lt=current_id).order_by('id').last()
    detail_view_name = app_name +':'+ ModelClass._meta.model_name +'-detail'

    if previous_record:
        return redirect(detail_view_name, pk=previous_record.pk)

    return redirect(detail_view_name, pk=current_id)  # Stay on the same record if none found


def first_record_view(request, app_name, model_name):
    ModelClass = apps.get_model(app_name, model_name)
    first_record = ModelClass.objects.order_by('id').first()
    detail_view_name = app_name +':'+ ModelClass._meta.model_name +'-detail'

    if first_record:
        return redirect(detail_view_name, pk=first_record.pk)


def last_record_view(request, app_name, model_name):
    ModelClass = apps.get_model(app_name, model_name)
    last_record = ModelClass.objects.order_by('id').last()
    detail_view_name = app_name +':'+ ModelClass._meta.model_name +'-detail'

    if last_record:
        return redirect(detail_view_name, pk=last_record.pk)


@login_required
def toggle_follow_view(request, app_name, model_name, current_id):
    ModelClass = apps.get_model(app_name, model_name)
    record = ModelClass.objects.get(id=current_id)
    user = request.user

    if user in record.followers.all():
        record.followers.remove(user)
        is_following = False
    else:
        record.followers.add(user)
        is_following = True

    return JsonResponse({"is_following": is_following})