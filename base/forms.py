import os
from django import forms
from django.contrib.auth.models import User, Group, Permission
from django.contrib.auth import password_validation
from django.forms.widgets import ClearableFileInput
from django_select2.forms import Select2Widget

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, HTML, Row, Column, Div, Button, Submit
from crispy_forms.bootstrap import PrependedText
from crispy_bootstrap5.bootstrap5 import FloatingField

from .models import UserProfile, Menu, UserMenuOrder
from django.urls import reverse

from .models import UserProfile



SELECTFILTER_CSS = {
    'all': (
        os.path.join('/static/admin/css/widgets.css'),
        os.path.join('/static/admin/css/responsive.css'),
        os.path.join('/static/css/custom.css')
    ),
}


class Helper(FormHelper):
    form_method = 'POST'
    form_class = 'form-horizontal'
    label_class = 'col-sm-12'
    field_class = 'col-sm-12'
    layout = Layout()

    def field_layout(self, *LayoutObject):
        self.layout = Layout(
            *LayoutObject,
            HTML(
                '<div class="btn-toolbar justify-content-center" role="toolbar" aria-label="Toolbar with button groups">'
                '<div class="btn-group m-1" role="group" aria-label="First group">'
                # '<button type="submit" class="btn btn-outline-danger" name="cancel" value="Update">'
                # '<i class="bi bi-backspace"></i> Cancel</button>'
                '<a href="{{ form.get_cancel_url }}" class="btn btn-outline-danger btn-sm"> <i class="bi bi-backspace"></i> Cancel </a>'
                '</div>'
                '<div class="btn-group m-1" role="group" aria-label="Second group">'
                '<button type="submit" class="btn btn-outline-primary btn-sm" name="submit" value="Update">'
                '<i class="bi bi-floppy"></i> Save</button>'
                '</div>'
                '</div>'
            )
        )

    # def field_layout(self, *LayoutObject):
    #     self.layout = Layout(
    #         *LayoutObject,
    #         Div(Div(Div(
    #         Submit('submit','Save',css_class='btn btn-primary'),
    #         Button('cancel','Cancel',css_class='btn btn-danger',onclick='window.history.back()'),
    #         css_class="card-body"),
    #         css_class='btn-group', aria_labelledby='Right group' ),
    #         css_class='btn-toolbar justify-content-center', aria_labelledby='Toolbar with button groups'
    #         )
    #     )


class CustomClearableFileInput(ClearableFileInput):
    template_name = "base/widgets/clearable_file_input.html"

class ClearableSelect2Widget(Select2Widget):

    def render(self, name, value, attrs=None, renderer=None):
        # Use the parent class's render method to get the basic Select2 input
        select2_html = super().render(name, value, attrs, renderer)
        # Add a clear button within the Select2 container.  We target the container.
        clear_button_html = """
            <script nonce="csms_custom_script">
                $(document).ready(function() {
                    var select2Input = $('#id_""" + name + """'); // Target by ID, safer
                    var select2Container = select2Input.next('.select2-container');
                    if (select2Container.length && !select2Container.find('.clear-select2').length) {
                        var clearButton = $('<button type="button" class="btn btn-sm btn-outline-secondary clear-select2">' +
                            '<i class="bi bi-backspace-fill"></i>' +  
                            '</button>');

                        select2Container.css({'position': 'relative','width': '100%'}); // Make container relative for absolute positioning
                        clearButton.appendTo(select2Container);

                        clearButton.on('click', function(e) {
                            e.preventDefault();
                            select2Input.val(null).trigger('change');
                            clearButton.hide(); // Hide the button after clearing.
                        });

                       //check if there is a value already on load, and show clear button accordingly
                        if (select2Input.val()) {
                            clearButton.show();
                        } else {
                            clearButton.hide();
                        }

                        select2Input.on('change', function() {
                            if ($(this).val()) {
                                clearButton.show();
                            } else {
                                clearButton.hide();
                            }
                        });
                    }
                

                $('#id_""" + name + """')
                    .parent('div')
                    .children('span')
                    .children('span')
                    .children('span')
                    .css('height', ' calc(3.5rem + 2px)');
                $('#id_""" + name + """')
                    .parent('div')
                    .children('span')
                    .children('span')
                    .children('span')
                    .children('span')
                    .css('margin-top', '18px');
                $('#id_""" + name + """')
                    .parent('div')
                    .find('label')
                    .css('z-index', '1');


                });

            </script>
        """
        return select2_html + clear_button_html


class UserProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = [
            'job',
            'phone',
            'country',
            'address',
            'company',
            'about',
            'image_file',
            'twitter',
            'facebook',
            'instagram',
            'linkedin'
        ]
        widgets = {
            'job': forms.TextInput(attrs={"placeholder": "Job", "class": "form-control"}),
            'phone': forms.TextInput(attrs={"placeholder": "Phone", "class": "form-control"}),
            'country': forms.TextInput(attrs={"placeholder": "Country", "class": "form-control"}),
            'address': forms.TextInput(attrs={"placeholder": "Address", "class": "form-control"}),
            'company': forms.TextInput(attrs={"placeholder": "Company", "class": "form-control"}),
            'about': forms.Textarea(attrs={"placeholder": "About",
                "class": "form-control", "style":"height: 200px;"}),
            'image_file': CustomClearableFileInput(attrs={"class": "form-control"}),
            'twitter': forms.TextInput(attrs={"placeholder": "", "class": "form-control"}),
            'facebook': forms.TextInput(attrs={"placeholder": "", "class": "form-control"}),
            'instagram': forms.TextInput(attrs={"placeholder": "", "class": "form-control"}),
            'linkedin': forms.TextInput(attrs={"placeholder": "", "class": "form-control"})
        }

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['user'].disabled = True

    class Media:
        css = SELECTFILTER_CSS
        js = ['/admin/jsi18n',]

    def __init__(self, *args, **kwargs):
        self.helper = Helper()
        self.helper.field_layout(
            Row(
                Column(Field('company')),
                Column(Field('job')),
                )
        )
        super(UserProfileForm, self).__init__(*args, **kwargs)

    def get_cancel_url(self):
        return reverse('userprofile-list')


class ProfileImageForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = [
            'image_file'
        ]
        widgets = {
            'user': forms.HiddenInput(),
            'image_file': CustomClearableFileInput(attrs={"class": "form-control"})
        }


class UserForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "User Name", "class": "form-control"}),disabled=True)
    first_name = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "First Name", "class": "form-control"}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Last Name", "class": "form-control"}))
    email = forms.EmailField( widget=forms.TextInput(attrs={"placeholder": "E-mail", "class": "form-control"}))
    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
        ]



# class UserProfileCreationForm(forms.ModelForm):
#     username = forms.CharField(max_length=150)
#     email = forms.EmailField()
#     password = forms.CharField(widget=forms.PasswordInput)
#     bio = forms.CharField(widget=forms.Textarea, required=False)

#     class Meta:
#         model = UserProfile
#         fields = ['bio']  # Fields from UserProfile

#     def save(self, commit=True):
#         user = User.objects.create_user(
#             username=self.cleaned_data['username'],
#             email=self.cleaned_data['email'],
#             password=self.cleaned_data['password']
#         )
#         user_profile = UserProfile(user=user, bio=self.cleaned_data['bio'])
#         if commit:
#             user_profile.save()
#         return user




class UserPasswordUpdateModelForm(forms.ModelForm):
    error_messages = {
        'password_mismatch': "The two password fields didn't match.",
    }
    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput,
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label="Password confirmation",
        widget=forms.PasswordInput,
        strip=False,
        help_text="Enter the same password as before, for verification.",
    )

    class Meta:
        model = User
        fields = ['password1', 'password2', ]

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def _post_clean(self):
        super()._post_clean()
        # Validate the password after self.instance is updated with form data
        # by super().
        password = self.cleaned_data.get('password2')
        if password:
            try:
                password_validation.validate_password(password, self.instance)
            except forms.ValidationError as error:
                self.add_error('password2', error)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class FormatForm(forms.Form):
    FORMAT_CHOICES = (
        ('xlsx', 'xlsx'),
        ('csv', 'csv'),
        ('json', 'json'),
    )
    format = forms.ChoiceField(choices=FORMAT_CHOICES, widget=forms.Select(attrs={'class':"form-select"}))


# import os
# from django import forms
# from django.contrib.admin.widgets import FilteredSelectMultiple
# from django.contrib.auth.models import User, Group, Permission
# from crispy_forms.helper import FormHelper
# from crispy_forms.layout import Layout, Field, HTML, Row, Column, Div, Button, Submit
# from crispy_forms.bootstrap import PrependedText
# from django.utils.translation import gettext_lazy as _
# from django.contrib.auth import password_validation
# from entities.models import Entity
# from .models import (
#     Access,
#     Menu,
#     Module,
#     ProxyUser,
#     GroupProfile)


# class ModuleForm(forms.ModelForm):
#     name = forms.CharField(max_length=120)
#     description = forms.CharField(
#         widget=forms.Textarea(
#             attrs={
#                 'rows': 5,
#                 'placeholder': 'Describe this module',
#             }),
#         max_length=4000,
#         help_text='The max length of the text is 4000.')
#     url = forms.CharField(max_length=120)
#     groups = forms.ModelMultipleChoiceField(
#         queryset=Group.objects.all(),
#         required=False,
#         widget=FilteredSelectMultiple(
#             "Groups",
#             is_stacked=False
#         )
#     )

#     class Media:
#         css = SELECTFILTER_CSS
#         js = ['/admin/jsi18n', ]

#     class Meta:
#         model = Module
#         fields = ['name', 'description', 'seq', 'url', 'groups']

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.helper = Helper()
#         self.helper.field_layout(
#             Field('name', placeholder='Name of Module'),
#             Field('description'),
#             PrependedText('seq', '#'),
#             Field('url', placeholder='xystum:home'),
#             Field('groups')
#         )


# class ModuleMenuForm(forms.ModelForm):
#     description = forms.CharField(
#         widget=forms.Textarea(
#             attrs={
#                 'rows': 5,
#                 'placeholder': 'Describe this menu',
#             }
#         ),
#         max_length=4000,
#         help_text='The max length of the text is 4000.'
#     )
#     groups = forms.ModelMultipleChoiceField(
#         queryset=Group.objects.all(),
#         required=False,
#         widget=FilteredSelectMultiple("Group", is_stacked=False)
#     )

#     class Media:
#         css = SELECTFILTER_CSS
#         js = ['/admin/jsi18n', ]

#     class Meta:
#         model = Menu
#         fields = [
#             'name',
#             'description',
#             'module',
#             'seq',
#             'allow_print',
#             'allow_excel',
#             'allow_filter',
#             'url',
#             'report_url',
#             'menu_type',
#             'groups'
#         ]

#     def __init__(self, *args, **kwargs):
#         self.helper = Helper()
#         self.helper.field_layout(
#             Field('module', css_class='col-12  my-0 py-0'),
#             Field(
#                 'name', placeholder='Name of menu item',
#                 css_class='col-12  my-0 py-0'),
#             Field('description', css_class='col-12  my-0 py-0'),
#             Row(
#                 Column(Field('seq'), css_class='col-md-3 my-0 py-0'),
#                 Column(Field(
#                     'menu_type',
#                     widget=forms.TextInput(attrs={'autofocus': 'autofocus'})
#                 ), css_class='col-md-3  my-0 py-0'),
#                 Column(Field('allow_print'), css_class='col-md-2 my-0 py-0'),
#                 Column(Field('allow_excel'), css_class='col-md-2 my-0 py-0'),
#                 Column(Field('allow_filter'), css_class='col-md-2 my-0 py-0'),
#             ),
#             Row(
#                 Column(
#                     Field('url', placeholder='xystum:menu-list'),
#                     css_class='col-md-6 my-0 py-0'),
#                 Column(
#                     Field('report_url', placeholder='xystum:menu-report'),
#                     css_class='col-md-6 my-0 py-0')),
#             Field('groups')
#         )
#         module_ = kwargs.pop('parent_id', '')
#         super(ModuleMenuForm, self).__init__(*args, **kwargs)
#         if module_:
#             self.initial['module'] = Module.objects.get(id=module_)
#             self.fields['module'].queryset = Module.objects.filter(id=module_)


# class UserModelForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ['first_name', 'last_name', 'email']

#     def __init__(self, *args, **kwargs):
#         self.helper = Helper()
#         self.helper.layout = Layout(
#             Field('first_name', placeholder='First Name'),
#             Field('last_name', placeholder='Last Name'),
#             Field('email', placeholder='E-mail'),
#             Div(
#                 Button(
#                     'cancel',
#                     '<i class="fas fa-key"></i> Change Password',
#                     css_class='btn btn-success btn-sm float-left',
#                     onclick="location.href='{% url 'xystum:password_change' %}'"),
#                 Submit(
#                     'submit',
#                     '<i class="fas fa-save"></i> Save',
#                     css_class='btn btn-primary btn-sm'),
#                 Button(
#                     'cancel',
#                     '<i class="fas fa-undo"></i> Cancel',
#                     css_class='btn btn-danger btn-sm',
#                     onclick='window.history.back()'),
#                 css_class='submit-row'
#             )
#         )
#         super(UserModelForm, self).__init__(*args, **kwargs)


# class UserUpdateModelForm(forms.ModelForm):
#     groups = forms.ModelMultipleChoiceField(
#         queryset=Group.objects.all(),
#         required=False,
#         widget=FilteredSelectMultiple("Group", is_stacked=False)
#     )
#     user_permissions = forms.ModelMultipleChoiceField(
#         queryset=Permission.objects.all(),
#         required=False,
#         widget=FilteredSelectMultiple("User Permission", is_stacked=False)
#     )

#     class Media:
#         css = SELECTFILTER_CSS
#         js = ['/admin/jsi18n', ]

#     class Meta:
#         model = User
#         fields = ['first_name', 'last_name', 'email', 'groups', 'user_permissions', ]

#     def __init__(self, *args, **kwargs):
#         self.helper = Helper()
#         self.helper.layout = Layout(
#             Row(
#                 Column(
#                     Field('first_name', placeholder='First Name'),
#                     css_class="col-sm-4"),
#                 Column(
#                     Field('last_name', placeholder='Last Name'),
#                     css_class="col-sm-4"),
#                 Column(
#                     Field('email', placeholder='E-mail'),
#                     css_class="col-sm-4")
#             ),
#             Field('groups'),
#             Field('user_permissions'),
#             HTML(
#                 u"""<hr>
#                 <div class='submit-row' style='margin-top:20px'>
#                 <button type="button" class="btn btn-success btn-sm float-left"
#                 onclick="location.href='{% url 'xystum:userpassword_update' object.id%}'">
#                 <i class="fas fa-key"></i> Change Password
#                 </button>
#                 <button class='btn btn-primary btn-sm' type='submit' name='_save'>
#                 <i class='fas fa-save'></i> Save</button>
#                 <button class='btn btn-danger btn-sm'
#                 type='button' onclick='window.history.back()'>
#                 <i class='fas fa-undo'></i> Cancel</button>
#                 </div>"""
#             )
#         )
#         super(UserUpdateModelForm, self).__init__(*args, **kwargs)


# class UserPasswordUpdateModelForm(forms.ModelForm):
#     error_messages = {
#         'password_mismatch': _("The two password fields didn't match."),
#     }
#     password1 = forms.CharField(
#         label=_("Password"),
#         strip=False,
#         widget=forms.PasswordInput,
#         help_text=password_validation.password_validators_help_text_html(),
#     )
#     password2 = forms.CharField(
#         label=_("Password confirmation"),
#         widget=forms.PasswordInput,
#         strip=False,
#         help_text=_("Enter the same password as before, for verification."),
#     )

#     class Meta:
#         model = ProxyUser
#         fields = ['password1', 'password2', ]

#     def __init__(self, *args, **kwargs):
#         self.helper = Helper()
#         self.helper.field_layout(
#             Div(
#                 HTML(
#                     u"""<div class="card-header">
#                     <h5>Change Password</h5></div>
#                     """),
#                 Div(
#                     HTML(
#                         u"""<div class="card-title">
#                         User: {{ object.get_full_name }}
#                         ({{ object.username }})
#                         </div>
#                         """),
#                     Field(
#                         'password1',
#                         placeholder='Password',
#                         css_class="col-sm-6"),
#                     Field(
#                         'password2',
#                         placeholder='Password',
#                         css_class="col-sm-6"),
#                     css_class="card-body"),
#                 css_class="card"))
#         super(UserPasswordUpdateModelForm, self).__init__(*args, **kwargs)

#     def clean_password2(self):
#         password1 = self.cleaned_data.get("password1")
#         password2 = self.cleaned_data.get("password2")
#         if password1 and password2 and password1 != password2:
#             raise forms.ValidationError(
#                 self.error_messages['password_mismatch'],
#                 code='password_mismatch',
#             )
#         return password2

#     def _post_clean(self):
#         super()._post_clean()
#         # Validate the password after self.instance is updated with form data
#         # by super().
#         password = self.cleaned_data.get('password2')
#         if password:
#             try:
#                 password_validation.validate_password(password, self.instance)
#             except forms.ValidationError as error:
#                 self.add_error('password2', error)

#     def save(self, commit=True):
#         user = super().save(commit=False)
#         user.set_password(self.cleaned_data["password1"])
#         if commit:
#             user.save()
#         return user


# class UserChoiceField(forms.ModelChoiceField):
#     def label_from_instance(self, obj):
#         return str(obj.id) + " - " + obj.username


# class GroupChoiceField(forms.ModelChoiceField):
#     def label_from_instance(self, obj):
#         return str(obj.id) + " - " + obj.name


# class AccessModelForm(forms.ModelForm):
#     group = GroupChoiceField(queryset=Group.objects.all().order_by('name'))
#     projects = forms.ModelMultipleChoiceField(
#         queryset=Entity.objects.filter(entitytype__code='PR'),
#         required=False,
#         widget=FilteredSelectMultiple("Project", is_stacked=False)
#     )

#     class Media:
#         css = SELECTFILTER_CSS
#         js = ['/admin/jsi18n', ]

#     class Meta:
#         model = Access
#         fields = ['group', 'projects']

#     def __init__(self, *args, **kwargs):
#         self.helper = Helper()
#         self.helper.field_layout(
#             Field('group', placeholder='Group'),
#             Field('projects'),
#         )
#         group_ = kwargs.pop('parent_id', '')
#         super(AccessModelForm, self).__init__(*args, **kwargs)
#         if group_:
#             self.initial['group'] = GroupProfile.objects.get(id=group_)
#             self.fields['group'].queryset = GroupProfile.objects.filter(
#                 id=group_)


# class UserProfileModelForm(forms.ModelForm):
#     error_messages = {
#         'password_mismatch': _("The two password fields didn't match."),
#     }
#     password1 = forms.CharField(
#         label=_("Password"),
#         strip=False,
#         widget=forms.PasswordInput,
#         help_text=password_validation.password_validators_help_text_html(),
#     )
#     password2 = forms.CharField(
#         label=_("Password confirmation"),
#         widget=forms.PasswordInput,
#         strip=False,
#         help_text=_("Enter the same password as before, for verification."),
#     )

#     class Media:
#         css = SELECTFILTER_CSS
#         js = ['/admin/jsi18n', ]

#     class Meta:
#         model = ProxyUser
#         fields = [
#             'username',
#             'first_name',
#             'last_name',
#             'email',
#             'password1',
#             'password2',
#         ]

#     def __init__(self, *args, **kwargs):
#         self.helper = Helper()
#         self.helper.field_layout(
#             Field('username', placeholder='User Name'),
#             Row(
#                 Column(
#                     Field('first_name', placeholder='First Name'),
#                     css_class="col-sm-4"),
#                 Column(
#                     Field('last_name', placeholder='Last Name'),
#                     css_class="col-sm-4"),
#                 Column(
#                     Field('email', placeholder='E-mail'),
#                     css_class="col-sm-4")
#             ),
#             Row(
#                 Column(
#                     Field('password1', placeholder='Password'),
#                     css_class="col-sm-6"),
#                 Column(
#                     Field('password2', placeholder='Password'),
#                     css_class="col-sm-6")
#             )
#         )
#         super(UserProfileModelForm, self).__init__(*args, **kwargs)

#     def clean_password2(self):
#         password1 = self.cleaned_data.get("password1")
#         password2 = self.cleaned_data.get("password2")
#         if password1 and password2 and password1 != password2:
#             raise forms.ValidationError(
#                 self.error_messages['password_mismatch'],
#                 code='password_mismatch',
#             )
#         return password2

#     def _post_clean(self):
#         super()._post_clean()
#         # Validate the password after self.instance is updated with form data
#         # by super().
#         password = self.cleaned_data.get('password2')
#         if password:
#             try:
#                 password_validation.validate_password(password, self.instance)
#             except forms.ValidationError as error:
#                 self.add_error('password2', error)

#     def save(self, commit=True):
#         user = super().save(commit=False)
#         user.set_password(self.cleaned_data["password1"])
#         if commit:
#             user.save()
#         return user
#         # return redirect(reverse('xystum:userprofile-list'))


# class GroupProfileModelForm(forms.ModelForm):
#     permissions = forms.ModelMultipleChoiceField(
#         queryset=Permission.objects.all(),
#         required=False,
#         widget=FilteredSelectMultiple("Permission", is_stacked=False)
#     )

#     class Meta:
#         model = GroupProfile
#         fields = ['name', 'permissions']

#     class Media:
#         css = SELECTFILTER_CSS
#         js = ['/admin/jsi18n', ]

#     def __init__(self, *args, **kwargs):
#         self.helper = Helper()
#         self.helper.field_layout(
#             Field('name', placeholder='Group Name'),
#             Field('permissions'),
#         )
#         super(GroupProfileModelForm, self).__init__(*args, **kwargs)



class MenuForm(forms.ModelForm):
    # sequence = forms.CharField(initial=(Menu.objects.all().order_by('sequence').last().sequence or 0) + 1)
    # menu_type = forms.ChoiceField(
    #     choices=
    #     )


    class Meta:
        model = Menu
        fields = ['module', 'menu_type', 'name', 'url_name','icon_class']
        widgets = {
            'menu_type': ClearableSelect2Widget(attrs={'class':"form-select", "data-placeholder": "select an option"})
        }

    class Media:
        css = SELECTFILTER_CSS
        js = ['/admin/jsi18n']


    def __init__(self, *args, **kwargs):
        self.helper = Helper()
        self.helper.field_layout(
            Row(
                Column(FloatingField('module'),css_class="col-lg-6"),
                Column(FloatingField('menu_type'),css_class="col-lg-6")
            ),
            Row(
                Column(FloatingField('name'),)
            ),
            Row(
                Column(FloatingField('url_name'),css_class="col-lg-6"),
                Column(FloatingField('icon_class'),css_class="col-lg-5 col-sm-10"),
                Column(
                HTML(
                '''
                <a class="dropdown-item d-flex align-items-center" href="{% url 'icons-bootstrap'%}" target="_blank">
                <i class="bi bi-info-square"></i>
                </a>
                '''
                ),css_class="col-1")
            )
        )
        super(MenuForm, self).__init__(*args, **kwargs)

    def get_cancel_url(self):
        return reverse('menu-list')

    def clean_url_name(self):
        menu_type = self.cleaned_data.get("menu_type")
        url_name = self.cleaned_data.get("url_name")
        if menu_type != 'Label' and not url_name:
            raise forms.ValidationError(f"Url name cannot be blank for menu type: {menu_type} ")
        return url_name


class UserMenuOrderForm(forms.ModelForm):
    # sequence = forms.CharField(initial=(Menu.objects.all().order_by('sequence').last().sequence or 0) + 1)
    # menu_type = forms.ChoiceField(
    #     choices=
    #     )


    class Meta:
        model = UserMenuOrder
        fields = ['userprofile', 'menu', 'order']
        

    def __init__(self, *args, **kwargs):
        self.helper = Helper()
        self.helper.field_layout(
            FloatingField('userprofile'),
            FloatingField('menu'),
            FloatingField('order')
        )
        userprofile_ = kwargs.pop('parent_id', '')
        super(UserMenuOrderForm, self).__init__(*args, **kwargs)
        if userprofile_:
            self.initial['userprofile'] = UserProfile.objects.get(pk=userprofile_)
            self.fields['userprofile'].queryset = UserProfile.objects.filter(pk=userprofile_)


    def get_cancel_url(self):
        return reverse('menu-list')
