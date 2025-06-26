from django.template import Library
from django.urls import reverse

from ..forms import PostForm
from ..models import Post
from ..views import add_url_for_obj


register = Library()


@register.inclusion_tag('comment/add_form.html', takes_context=True)
def post_form(context, obj):
    """
    Renders a "upload document" form.
    The user must own ``attachments.add_attachment permission`` to add
    attachments.
    """

    if context['user'].has_perm('comment.add_post'):
        return {
            'form': PostForm(),
            'form_url': add_url_for_obj(obj),
            'next': context.request.build_absolute_uri(),
        }
    else:
        return {'form': None}


@register.inclusion_tag('comment/delete_link.html', takes_context=True)
def post_delete_link(context, post):
    """
    Renders a html link to the delete view of the given attachment. Returns
    no content if the request-user has no permission to delete attachments.
    The user must own either the ``attachments.delete_attachment`` permission
    and is the creator of the attachment, that he can delete it or he has
    ``attachments.delete_foreign_attachments`` which allows him to delete all
    attachments.
    """

    if context['user'].has_perm('comment.delete_foreign_posts') or (
        context['user'] == post.created_by and
        context['user'].has_perm('comment.delete_post')
    ):
        return {
            'next': context.request.build_absolute_uri(),
            'delete_url': reverse(
                'comment:delete', kwargs={'post_pk': post.pk}
            ),
            'modal_pk': post.pk,
        }
    return {'delete_url': None}


@register.simple_tag
def posts_count(obj):
    """
    Counts attachments that are attached to a given object::
        {% attachments_count obj %}
    """
    return Post.objects.posts_for_object(obj).count()


@register.simple_tag
def get_posts_for(obj, *args, **kwargs):
    """
    Resolves attachments that are attached to a given object. You can specify
    the variable name in the context the attachments are stored using the `as`
    argument.
    Syntax::
        {% get_attachments_for obj as "my_attachments" %}
    """
    return Post.objects.posts_for_object(obj)
