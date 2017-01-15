from django.contrib import admin

# Register your models here.
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib import admin
from django.contrib.auth.models import Group

from DocumentsFlowApp.models import Group as My_group

from DocumentsFlowApp.models import MyUser
from DocumentsFlowApp.models import Flux
from DocumentsFlowApp.models import Assigment
from DocumentsFlowApp.models import Process
from DocumentsFlowApp.models import Task
from DocumentsFlowApp.models import Template
from DocumentsFlowApp.models import Document

class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = MyUser
        fields = ('group', 'username', 'email', 'password', )

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = MyUser
        fields = ('username', 'email', 'password', 'group', 'is_active', 'is_admin')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('username', 'email', 'password', 'group', 'is_admin', 'is_reader', 'is_manager', 'is_contributor')
    list_filter = ('is_admin', 'is_reader', 'is_manager', 'is_contributor')
    fieldsets = (
        (None, {'fields': ('username', 'password', 'group')}),
        ('Personal info', {'fields': ('email',)}),
        ('Permissions', {'fields': ('is_admin', 'is_reader', 'is_manager', 'is_contributor')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2')}
        ),
    )
    search_fields = ('username',)
    ordering = ('username',)
    filter_horizontal = ()


class GroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ['id', 'name']


class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'status')
    list_display_links = ['id', 'status']


class FluxAdmin(admin.ModelAdmin):
    list_display = ('id', 'documents')
    list_display_links = ['id', 'documents']


class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'documentTypes')
    list_display_links = ['id', 'documentTypes']


class ProcessAdmin(admin.ModelAdmin):
    list_display = ('id', 'starter', 'flux')
    list_display_links = ['id', 'starter', 'flux']


class TemplateAdmin(admin.ModelAdmin):
    list_display = ('id', 'keys')
    list_display_links = ['id', 'keys']


class DocumentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'path', 'version', 'status', 'date', 'owner', 'type', 'template', 'templateValues', 'task')
    list_display_links = ['id', 'name', 'path', 'version', 'status', 'date', 'owner', 'type', 'template', 'templateValues', 'task']


# Now register the new UserAdmin...
admin.site.register(MyUser, UserAdmin)
admin.site.register(My_group, GroupAdmin)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)

admin.site.register(Flux, FluxAdmin)
admin.site.register(Assigment, AssignmentAdmin)
admin.site.register(Process, ProcessAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(Template, TemplateAdmin)
admin.site.register(Document, DocumentAdmin)
