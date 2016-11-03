from django.contrib import admin
from django.contrib.admin.forms import AdminAuthenticationForm
from django import forms


class NavigatorLoginForm(AdminAuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'autocomplete': 'off'}))


admin.site.login_form = NavigatorLoginForm
