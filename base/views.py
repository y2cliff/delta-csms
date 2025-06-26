from django.contrib import messages
from django.contrib.auth import logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views  import LoginView
from django.db import transaction
from django.db.models import ProtectedError
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, FormView
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormMixin

from django_filters.views import FilterView
from django_tables2 import SingleTableMixin
from django_tables2.export.views import ExportMixin
from django_tables2.paginators import LazyPaginator
# from wkhtmltopdf.views import PDFTemplateView

from .filters import UserProfileFilter
from .forms import UserForm, UserProfileForm, ProfileImageForm, FormatForm
from .mixins import ContextTitleMixin
from .models import UserProfile, Menu, UserMenuOrder
from .tables import UserProfileTable
from base.admin import UserProfileResource
from base.forms import FormatForm


# class BaseView(ContextTitleMixin, TemplateView):
#     template_name = ''


# class BaseListView(ContextTitleMixin, ListView):
#     model = Menu
#     template_name = 'base/index.html'
#     # context_object_name = 'works'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['model_name'] = self.model._meta.model_name
#         return context


# class BaseFormView(ContextTitleMixin, FormView):
#     # success_url = "success"
#     form_class = FormatForm

#     def get_success_url(self):
#         return reverse(self.success_url)


# class BaseDetailView(ContextTitleMixin, DetailView):
#     model = None
#     # success_url = "success"


# class BaseCreateView(ContextTitleMixin, CreateView):
#     model = None
#     # success_url = "success"


# class BaseUpdateView(ContextTitleMixin, UpdateView):
#     model = None
#     # success_url = "success"


# class BaseDeleteView(ContextTitleMixin, DeleteView):
#     model = None
#     # success_url = "success"


# class HomeView(BaseListView):
#     template_name = "base/index.html"    
#     page_name = 'Modules'
#     page_title = 'Select Module'

#     def get_queryset(self):
#         queryset = Menu.objects.filter(menu_type = 'Modules' , user = self.request.user)
#         return queryset


class MyLoginView(LoginView):
    template_name='login.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        remember_me = self.request.POST.get("remember_me")
        if remember_me:
            self.request.session.set_expiry(60 * 60 * 24 * 30)  # One month
        else:
            self.request.session.set_expiry(0)  # Expires when browser closes
        return response


def logoutview(request):
    logout(request)
    return redirect('home')


class BaseMixin:
    module = 'base'
    page_name = 'Modules'
    page_title = 'Select Module'
    parent_menu = []

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module'] = self.module
        context['user_menus'] = UserMenuOrder.objects.my_module_menus(
            module=self.module, 
            user=self.request.user) or None
        context['page_title'] = self.page_title
        context['parent_menu'] = self.parent_menu
        context['page_name'] = self.page_name
        return context


# Xystum
class TemplateHomeView(LoginRequiredMixin, BaseMixin, ListView):
    template_name = "base/index.html"    
    model = UserProfile


class TemplateListView(LoginRequiredMixin, SingleTableMixin, BaseMixin, ExportMixin, FilterView):
    model = UserProfile
    table_class = UserProfileTable
    template_name = 'list.html'
    table_pagination = False
    paginator_class = LazyPaginator
    export_name = model.__name__
    filterset_class = UserProfileFilter
    model_resource = UserProfileResource

    def get_context_data(self, **kwargs):
        context = super(TemplateListView, self).get_context_data(**kwargs)
        self.export_name = self.model.__name__ + '_list'
        context['can_add'] = True if self.request.user.has_perm(
            self.model._meta.app_label + '.add_' + self.model._meta.model_name) else False
        context['form'] = FormatForm(None)
        return context

    def post(self, request, *args, **kwargs):
        if 'download' in request.POST:
            qs = self.get_queryset() #filtering done here
            dataset = self.model_resource().export(qs)

            filename = self.model.__name__ + '_List'

            format = request.POST.get('format')

            if format == 'xlsx':
                ds = dataset.xlsx
            elif format == 'csv':
                ds = dataset.csv
            else:
                ds = dataset.json

            response = HttpResponse(ds, content_type=f"{format}")
            response['Content-Disposition']= f"attachment; filename={filename}.{format}"
            return response


class TemplateCreateView(LoginRequiredMixin, PermissionRequiredMixin, BaseMixin, CreateView):
    model = UserProfile
    template_name = 'create.html'
    form_class = UserProfileForm
    permission_required = ''


    def form_valid(self, form):
        if 'cancel' in self.request.POST:
            url = self.request.META.get('HTTP_REFERER')
            return HttpResponseRedirect(url.replace("create/",""))
        if form.is_valid():
            instance = form.save(commit=False)
            model=self.model.__name__,
            success_message = 'SUCCESS! {model} "{instance}" was successfully created!'
            messages.success(self.request, success_message.format(
                model=model,
                instance=instance)
            )
            return super(TemplateCreateView, self).form_valid(form)
        else:
            return HttpResponseRedirect(url.replace("create/",""))

    def form_invalid(self, form):
        if 'cancel' in self.request.POST:
            url = self.request.META.get('HTTP_REFERER')
            return HttpResponseRedirect(url.replace("create/",""))
        return super(TemplateCreateView, self).form_invalid(form)
           

class TemplateChildCreateView(TemplateCreateView):
    parent_model = User

    def get_form_kwargs(self):
        kwargs = super(TemplateChildCreateView, self).get_form_kwargs()
        kwargs.update({"parent_id": self.kwargs['parent_id']})
        return kwargs

    def get_context_data(self, **kwargs):
        context = (super(TemplateChildCreateView, self).get_context_data(**kwargs))
        context['parent_object'] = (
            self.parent_model.objects.get(pk=self.kwargs['parent_id']))
        return context


class TemplateDetailView(LoginRequiredMixin, PermissionRequiredMixin, BaseMixin, DetailView):
    model = UserProfile
    template_name = 'home.html'
    permission_required = ''
    allow_delete = allow_change = True

    def get_context_data(self, **kwargs):
        context = super(TemplateDetailView, self).get_context_data(**kwargs)
        context['can_change'] = True if self.request.user.has_perm(
            self.model._meta.app_label + '.change_' + self.model._meta.model_name) else False
        context['can_delete'] = True if self.request.user.has_perm(
            self.model._meta.app_label + '.delete_' + self.model._meta.model_name) else False
        context['allow_delete'] = self.allow_delete
        context['allow_change'] = self.allow_change
        return context

    def get_object(self):
        pk_ = self.kwargs.get("pk")
        return get_object_or_404(self.model, pk=pk_)


class TemplateChildDetailView(TemplateDetailView):
    parent_model = UserProfile

    def get_form_kwargs(self):
        kwargs = super(TemplateChildDetailView, self).get_form_kwargs()
        kwargs.update({"parent_id": self.kwargs['parent_id']})
        return kwargs

    def get_context_data(self, **kwargs):
        context=(super(TemplateChildDetailView, self).get_context_data(**kwargs))
        context['parent_object']=(
            self.parent_model.objects.get(id=self.kwargs['parent_id']))
        return context


class TemplateUpdateView(LoginRequiredMixin, PermissionRequiredMixin, BaseMixin, UpdateView):
    model = UserProfile
    template_name = 'create.html'
    permission_required = ''

    # def get_object(self):
    #     id_ = self.kwargs.get("pk")
    #     return get_object_or_404(self.model, id=id_)

    def form_valid(self, form):
        if 'cancel' in self.request.POST:
            return HttpResponseRedirect(self.get_success_url())
        instance = form.save(commit=False)
        success_message = 'SUCCESS! {model} "{instance}" was successfully updated!'
        messages.success(self.request, success_message.format(
            model=self.model.__name__,
            instance=instance)
        )
        instance.save()
        return super(TemplateUpdateView, self).form_valid(form)


class TemplateChildUpdateView(TemplateUpdateView):
    parent_model = UserProfile

    def get_form_kwargs(self):
        kwargs = super(TemplateChildUpdateView, self).get_form_kwargs()
        kwargs.update({"parent_id": self.kwargs['parent_id']})
        return kwargs

    def get_context_data(self, **kwargs):
        context = (super(TemplateChildUpdateView, self).get_context_data(**kwargs))
        context['parent_object'] = (
            self.parent_model.objects.get(pk=self.kwargs['parent_id']))
        return context


class TemplateDeleteView(LoginRequiredMixin, PermissionRequiredMixin, BaseMixin, DeleteView):
    model = UserProfile
    parent_model = UserProfile
    template_name = 'delete.html'
    url_path = 'xystum:home'
    permission_required = ''

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(self.model, pk=id_)

    def get_success_url(self):
        return reverse(self.url_path)

    def delete(self, request, *args, **kwargs):
        self.object = instance = self.get_object()
        success_url = self.get_success_url()


        if (
            request.user.has_perm(self.model._meta.app_label + '.delete_' + self.model._meta.model_name) and
            request.user == instance.created_by
        ) or request.user.has_perm(self.model._meta.app_label + '.delete_foreign' + self.model._meta.model_name):
            instance.delete()
            messages.success(request, gettext(success_message))
            next_ = request.GET.get('next') or '/'
            return HttpResponseRedirect(next_)

        try:
            if (
                request.user.has_perm(self.model._meta.app_label + '.delete_' + self.model._meta.model_name) and
                request.user == instance.created_by
            ) or request.user.has_perm(self.model._meta.app_label + '.delete_foreign' + self.model._meta.model_name):
                instance.delete()
                success_message = 'SUCCESS! {model} "{instance}" was successfully deleted!'
                messages.success(self.request, success_message.format(
                    model=self.model.__name__,
                    instance=instance)
            )
        except ProtectedError:
            messages.error(
                self.request,
                'ERROR! {model} "{instance}" is protected! \
                 Remove all references to other records first.'.format(
                    model=self.model.__name__,
                    instance=instance)
            )
            return HttpResponseRedirect(request.get_full_path())
        return HttpResponseRedirect(success_url)


class TemplateChildDeleteView(TemplateDeleteView):
    parent_model = UserProfile

    def get_success_url(self):
        parent = self.parent_model.objects.get(id=self.kwargs['parent_id'])
        return reverse(self.url_path, kwargs={'id': parent.id})

    def get_context_data(self, **kwargs):
        context = (
            super(TemplateChildDeleteView, self).get_context_data(**kwargs))
        context['parent_object'] = (
            self.parent_model.objects.get(pk=self.kwargs['parent_id']))
        return context


# @login_required()
# @transaction.atomic()
# def update_profile(request):
#     success_message = 'SUCCESS! Your profile was successfully updated!'
#     fail_message = 'FAILED! Please correct the error below.'
#     if request.method == 'POST':
#         user_form = UserModelForm(request.POST, instance=request.user)
#         if user_form.is_valid():
#             user_form.save()
#             messages.success(request, success_message)
#             return redirect('xystum:home')
#         else:
#             messages.warning(request, fail_message)
#     else:
#         user_form = UserModelForm(instance=request.user)
#     context = {
#         'user_form': user_form,
#         'active_module': Module.objects.get(pk=1),
#         'menu_name': 'My Profile'
#     }
#     return render(request, 'xystum/my_profile.html', context)


# class ReportTemplateView(LoginRequiredMixin, PDFTemplateView):
#     filename = template_name = report_title = ''
#     model = UserProfile
#     cmd_options = {
#         'margin-top': 3,
#         'header-right': '[page]/[toPage]',
#         'footer-center': '',
#     }
#     show_content_in_browser = True

#     def get_context_data(self, **kwargs):
#         context = super(ReportTemplateView, self).get_context_data(**kwargs)
#         context['report_title'] = self.report_title
#         return context


class MyProfileView(TemplateHomeView):
    template_name = "base/page-userprofile.html"
    page_title="Profile"
    page_name="Profile"
    parent_menu=[["Users",'my-profile']]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_ = self.request.user
        userprofile_ =  user_.profile
        context["pform"] = UserForm(instance=user_)
        context["dform"] = UserProfileForm(instance=userprofile_)
        context["iform"] = ProfileImageForm(instance=userprofile_)
        context["uform"] = PasswordChangeForm(user_)
        return context

    def post(self, request, *args, **kwargs):
        if 'submit' in request.POST:
            user_ = User.objects.get(username=request.user.username)
            user_form_class = UserForm(request.POST or None, instance=request.user)
            
            # userprofile_form_class = UserProfileForm(request.POST or None, instance=request.user.userprofile)
            if user_form_class.is_valid():
                user_form_class.save()
                userprofile_form_class = UserProfileForm(request.POST or None, instance=request.user.profile)
                if userprofile_form_class.is_valid():
                    userprofile_form_class.save()
            return HttpResponseRedirect(self.request.path_info) 
        if 'submit_image' in request.POST:
            user_ = request.user
            instance = UserProfile.objects.get(user=user_)
            profileimage_form_class = ProfileImageForm(request.POST or None, request.FILES, instance=instance)
            if profileimage_form_class.is_valid():
                profileimage_form_class.save()
        if 'delete_image' in request.POST:
            user_ = request.user
            instance = UserProfile.objects.get(user=user_)
            if instance:
                instance.image_file.delete(save=True)
                # instance.save()
        if 'change_password' in request.POST:
            form = PasswordChangeForm(request.user, request.POST)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)  # Prevents logout after password change
                messages.success(request, "Password successfully changed")
                return redirect("password_change_done")
            else:
                messages.error(request, "Unable to change password. Please see error message.")
                return render(request, "base/page-userprofile.html",{"uform":form})
        else:
            form = PasswordChangeForm(request.user)
        # return render(request, "change_password.html", {"form": form})

        return HttpResponseRedirect(self.request.path_info) 


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User

    def get_object(self):
        id_ = self.kwargs.get('id')
        return get_object_or_404(self.model, id=id_)

    def form_valid(self, form):
        instance = form.save(commit=False)
        # instance.updated_by = self.request.user
        success_message = 'SUCCESS! {model} "{instance}" was successfully updated!'
        messages.success(self.request, success_message.format(
            model=self.model.__name__,
            instance=instance)
        )
        return super(UserUpdateView, self).form_valid(form)


def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Prevents logout after password change
            return redirect("password_change_done")
    else:
        form = PasswordChangeForm(request.user)
    return render(request, "change_password.html", {"form": form})


# from django.contrib.auth import get_user_model
# from your_app.models import Menu, UserMenu

# # Get the user instance
# User = get_user_model()
# user = User.objects.get(username="example_user")  # Modify as needed

# # Get all available menu items
# menu_items = Menu.objects.all()  # Adjust queryset if needed

# # Iterate through the menu list and populate UserMenu table
# for menu in menu_items:
#     if not UserMenu.objects.filter(user=user, menu=menu).exists():
#         UserMenu.objects.create(user=user, menu=menu)

# print("UserMenu table populated successfully.")
