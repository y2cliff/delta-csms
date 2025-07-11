"""
URL configuration for xys project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.views import i18n
from django.views.static import serve
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin/jsi18n/', i18n.JavaScriptCatalog.as_view(), name='jsi18n'),
    path("select2/", include("django_select2.urls")),

    path('', include('base.urls')),
    path('document/', include('document.urls')),
    path('comment/', include('comment.urls')),
    # path('project/', include('project.urls')),
    # path('cit/', include('cit.urls')),
    # path('inventory/', include('inventory.urls')),
]

@login_required
def protected_serve(request, path, document_root=None, show_indexes=False):
    return serve(request, path, document_root, show_indexes)


# This will serve the static and media files even when Debug Mode is False
if settings.DEBUG is False:
    urlpatterns += [
        re_path(
            r'^%s(?P<path>.*)$' % settings.STATIC_URL[1:],
            protected_serve,
            {'document_root': settings.STATIC_ROOT}
        ),
    ]
    urlpatterns += [
        re_path(
            r'^%s(?P<path>.*)$' % settings.MEDIA_URL[1:],
            protected_serve,
            {'document_root': settings.MEDIA_ROOT}
        ),
    ]

