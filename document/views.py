# from __future__ import unicode_literals

import os

from django.apps import apps
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.template.context import RequestContext
from django.urls import reverse
from django.utils.translation import gettext
from django.views.decorators.http import require_POST

from .forms import DocumentForm
from .models import Document
from .validators import validate_max_size, validate_type


def add_url_for_obj(obj):
    return reverse(
        'document:add',
        kwargs={
            'app_label': obj._meta.app_label,
            'model_name': obj._meta.model_name,
            'pk': obj.pk,
        },
    )


def remove_file_from_disk(f):
    if getattr(
        settings, 'DELETE_DOCUMENTS_FROM_DISK', False
    ) and os.path.exists(f.path):
        try:
            os.remove(f.path)
        except OSError:
            pass


@require_POST
@login_required
def add_document(
    request,
    app_label,
    model_name,
    pk,
    template_name='document/add_form.html',
    extra_context=None,
):
    next_ = request.POST.get('next', '/')

    if not request.user.has_perm('document.add_document'):
        return HttpResponseRedirect(next_)

    model = apps.get_model(app_label, model_name)
    obj = get_object_or_404(model, pk=pk)
    form = DocumentForm(request.POST, request.FILES)
    success_message = 'Your attached document was successfully uploaded.'
    fail_message = 'File/s contains invalid Size or Format, unable to upload your file.'
    files = request.FILES.getlist('document_file')
    if form.is_valid():
        for f in files:
            try:
                validate_max_size(f)
                validate_type(f)
                instance = Document(
                    content_type=ContentType.objects.get_for_model(obj),
                    object_id=obj.id,
                    content_object=obj,
                    creator=request.user,
                    document_file=f
                    )
                instance.save()
            except:
                messages.error(request, gettext(fail_message))
                return HttpResponseRedirect(next_)
            # form.save(request, obj)
        messages.success(request, gettext(success_message))
        return HttpResponseRedirect(next_)
    else:
        messages.error(request, gettext(fail_message))
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
def delete_document(request, document_pk):
    g = get_object_or_404(Document, pk=document_pk)
    success_message = 'Your attached document was successfully deleted.'

    if (
        request.user.has_perm('document.delete_document') and
        request.user == g.creator
    ) or request.user.has_perm('document.delete_foreign_documents'):
        remove_file_from_disk(g.document_file)
        g.delete()
        messages.success(request, gettext(success_message))
    next_ = request.GET.get('next') or '/'
    return HttpResponseRedirect(next_)
