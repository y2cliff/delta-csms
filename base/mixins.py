from django.views.generic.base import ContextMixin
from django.contrib.auth.mixins import LoginRequiredMixin


class ContextTitleMixin(LoginRequiredMixin, ContextMixin):
    page_title = ''
    page_name = ''
    parent_menu = {}


    def get_page_title(self):
        return self.page_title

    def get_page_name(self):
        return self.page_name

    def get_parent_menu(self):
        return self.parent_menu

    def get_context_data(self, **kwargs):
        """Insert the form into the context dict."""
        kwargs['page_title'] = self.get_page_title()
        kwargs['parent_menu'] = self.get_parent_menu()
        kwargs['page_name'] = self.get_page_name()
        return super().get_context_data(**kwargs)
