from django.contrib import admin
from django.contrib.admin.forms import AdminAuthenticationForm
from django import forms


class NavigatorLoginForm(AdminAuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'autocomplete': 'off'}))


admin.site.login_form = NavigatorLoginForm


def get_actions_replacer(orig_func):
    def fixed_get_actions(self, request):
        """
        Remove the delete action (if present) if user does not have the
        necessary permission
        """

        # Get the base actions
        actions = orig_func(self, request)
        # Get the app label and model name to form the permission name
        app_label = self.model._meta.app_label
        model_name = self.model._meta.model_name
        perm = "%s.delete_%s" % (app_label, model_name)
        # If the user does not have the specific delete perm, remove the action
        if not request.user.has_perm(perm):
            if 'delete_selected' in actions:
                del actions['delete_selected']

        return actions
    return fixed_get_actions

admin.ModelAdmin.get_actions = get_actions_replacer(admin.ModelAdmin.get_actions)
