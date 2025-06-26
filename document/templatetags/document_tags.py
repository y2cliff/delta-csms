from django.conf import settings
from django.template import Library
from django.urls import reverse

from document.forms import DocumentForm
from document.models import Document
from document.views import add_url_for_obj


register = Library()


@register.inclusion_tag('document/add_form.html', takes_context=True)
def document_form(context, obj):
    """
    Renders a "upload document" form.
    The user must own ``attachments.add_attachment permission`` to add
    attachments.
    """

    if context['user'].has_perm('document.add_document'):
        return {
            'form': DocumentForm(),
            'form_url': add_url_for_obj(obj),
            'next': context.request.build_absolute_uri(),
            'file_types': settings.FILE_UPLOAD_ALLOWED_TYPES,
            'max_size': settings.FILE_UPLOAD_MAX_SIZE/1024/1024,
        }
    else:
        return {'form': None}


@register.inclusion_tag('document/delete_link.html', takes_context=True)
def document_delete_link(context, document):
    """
    Renders a html link to the delete view of the given attachment. Returns
    no content if the request-user has no permission to delete attachments.
    The user must own either the ``attachments.delete_attachment`` permission
    and is the creator of the attachment, that he can delete it or he has
    ``attachments.delete_foreign_attachments`` which allows him to delete all
    attachments.
    """

    if context['user'].has_perm('document.delete_foreign_documents') or (
        context['user'] == document.creator and
        context['user'].has_perm('document.delete_document')
    ):
        return {
            'next': context.request.build_absolute_uri(),
            'delete_url': reverse(
                'document:delete', kwargs={'document_pk': document.pk}
            ),
            'modal_pk': document.pk,
        }
    return {'delete_url': None}


@register.simple_tag
def documents_count(obj):
    """
    Counts attachments that are attached to a given object::
        {% attachments_count obj %}
    """
    return Document.objects.documents_for_object(obj).count()


@register.simple_tag
def get_documents_for(obj, *args, **kwargs):
    """
    Resolves attachments that are attached to a given object. You can specify
    the variable name in the context the attachments are stored using the `as`
    argument.
    Syntax::
        {% get_attachments_for obj as "my_attachments" %}
    """
    return Document.objects.documents_for_object(obj)
