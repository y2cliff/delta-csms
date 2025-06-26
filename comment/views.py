import os

from django.apps import apps
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.template.context import RequestContext
from django.urls import reverse
from django.utils.translation import gettext
from django.views.decorators.http import require_POST

from .forms import PostForm
from .models import Post


def add_url_for_obj(obj):
    return reverse(
        'comment:add',
        kwargs={
            'app_label': obj._meta.app_label,
            'model_name': obj._meta.model_name,
            'pk': obj.pk,
        },
    )


@require_POST
@login_required
def add_post(
    request,
    app_label,
    model_name,
    pk,
    template_name='comment/add_form.html',
    extra_context=None,
):
    next_ = request.POST.get('next', '/')

    if not request.user.has_perm('comment.add_post'):
        return HttpResponseRedirect(next_)

    model = apps.get_model(app_label, model_name)
    obj = get_object_or_404(model, pk=pk)
    form = PostForm(request.POST, request.FILES)
    success_message = 'Your comment was successfully posted.'

    if form.is_valid():
        form.save(request, obj)
        messages.success(request, gettext(success_message))
        return HttpResponseRedirect(next_)

    template_context = {
        'form': form,
        'form_url': add_url_for_obj(obj),
        'next': next_,
    }
    template_context.update(extra_context or {})

    return render(
        template_name, template_context, RequestContext(request)
    )


@login_required
def delete_post(request, post_pk):
    g = get_object_or_404(Post, pk=post_pk)
    success_message = 'Your comment was successfully deleted.'

    if (
        request.user.has_perm('comment.delete_post') and
        request.user == g.created_by
    ) or request.user.has_perm('comment.delete_foreign_posts'):
        g.delete()
        messages.success(request, gettext(success_message))
    next_ = request.GET.get('next') or '/'
    return HttpResponseRedirect(next_)
