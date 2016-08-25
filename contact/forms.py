from django import forms

from django.core.mail import EmailMessage
from django.conf import settings


class ContactForm(forms.Form):
    contact_name = forms.CharField(required=True, label="Name")
    contact_email = forms.EmailField(required=True, label="Email")
    originating_page = forms.CharField(required=False, widget=forms.HiddenInput())
    content = forms.CharField(
        label="Feedback",
        required=True,
        widget=forms.Textarea
    )
