import os
from django import forms
from django.contrib.auth.models import User, Group, Permission
from django.contrib.auth import password_validation
from django.forms.widgets import ClearableFileInput
from django_select2.forms import Select2Widget
from django.contrib.admin.widgets import FilteredSelectMultiple

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, HTML, Row, Column, Div, Button, Submit
from crispy_forms.bootstrap import PrependedText
from crispy_bootstrap5.bootstrap5 import FloatingField

from .models import UserProfile, GroupProfile, Menu, Department
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
    # username = forms.CharField()
    # password = forms.CharField(widget=forms.PasswordInput)
    # email = forms.EmailField()
    menu = forms.ModelMultipleChoiceField(
        queryset = Menu.objects.all(),
        required=False,
        widget=FilteredSelectMultiple("Menu", is_stacked=False)
    )

    class Meta:
        model = UserProfile
        fields = [
            # 'username',
            # 'password',
            'user',
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
            'linkedin',
            'menu'
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
                Column(FloatingField('user'),css_class="col-12")
            ),
            Row(
                Column(FloatingField('company'),css_class="col-6"),
                Column(FloatingField('job'),css_class="col-6"),
                ),
            Row(
                Column(FloatingField('menu'),css_class="col-12")
            )
        )
        parent_ = kwargs.pop('parent_id','')
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields['user'].queryset = User.objects.filter(profile__isnull=True)
        if parent_:
            self.initial['user'] = User.objects.get(pk=parent_)
            self.fields['user'].queryset = User.objects.filter(pk=parent_)
            self.fields['user'].required = True
        self.fields["user"].label_from_instance = lambda obj: obj.get_full_name() or obj.username

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

class GroupProfileForm(forms.ModelForm):
    menu = forms.ModelMultipleChoiceField(
        queryset = Menu.objects.all(),
        required=False,
        widget=FilteredSelectMultiple("Menu", is_stacked=False)
    )

    class Meta:
        model = GroupProfile
        fields = [
            'group',
            'name',
            'menu'
        ]

    class Media:
        css = SELECTFILTER_CSS
        js = ['/admin/jsi18n',]

    def __init__(self, *args, **kwargs):
        self.helper = Helper()
        self.helper.field_layout(
            Row(
                Column(Field('group'),css_class="col-3"),
                Column(Field('name'),css_class="col-9"),
                ),
            Row(
                Column(FloatingField('menu'),css_class="col-12")
            )
        )
        parent_ = kwargs.pop('parent_id','')
        super(GroupProfileForm, self).__init__(*args, **kwargs)
        self.fields['group'].queryset = Group.objects.filter(profile__isnull=True)
        if parent_:
            self.initial['group'] = Group.objects.get(pk=parent_)
            self.fields['group'].queryset = Group.objects.filter(pk=parent_)
            self.fields['group'].required = True

    def get_cancel_url(self):
        return reverse('groupprofile-list')


class MenuForm(forms.ModelForm):
    class Meta:
        model = Menu
        fields = ['code','module', 'menu_type', 'name', 'url_name','icon_class']
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
                Column(FloatingField('code'),css_class="col-lg-4"),
                Column(FloatingField('module'),css_class="col-lg-4"),
                Column(FloatingField('menu_type'),css_class="col-lg-4")
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

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['code', 'name']

    def __init__(self, *args, **kwargs):
        self.helper = Helper()
        self.helper.field_layout(
            FloatingField('code'),
            FloatingField('name')
        )
        super(DepartmentForm, self).__init__(*args, **kwargs)

    def get_cancel_url(self):
        return reverse('department-list')
