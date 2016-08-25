import smtplib
from django.shortcuts import redirect
from django.views.generic.edit import FormView
from django.views.generic.base import TemplateView
from django.core.urlresolvers import reverse_lazy
from django.conf import settings
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from .forms import ContactForm


def send_email(source,
               to_address,
               subject,
               body,
               reply_to_address=None):
    smtp = None
    resp = None
    try:
        smtp = smtplib.SMTP(settings.SMTP_SERVER)
        smtp.starttls()
        smtp.login(
            settings.SMTP_USER,
            settings.SMTP_PWD)
        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['From'] = source
        msg['To'] = to_address
        body_plain = MIMEText(body, 'plain')
        msg.attach(body_plain)
        resp = smtp.sendmail(source, to_address, msg.as_string())
    finally:
        if smtp:
            try:
                smtp.quit()
            except:
                pass
    return resp


class ContactView(FormView):
    template_name = 'contact.html'
    form_class = ContactForm

    def form_valid(self, form):
        op = form.cleaned_data.get('originating_page')
        body = "{0}\n{1}\n{2}\n{3}".format(
            op,
            form.cleaned_data.get('contact_name'),
            form.cleaned_data.get('contact_email'),
            form.cleaned_data.get('content'))
        resp = send_email(
            settings.FEEDBACK_FROM,
            settings.FEEDBACK_TO,
            "Navigator Feedback",
            body)

        redirect_url = op if op else '/'
        return redirect(redirect_url)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['initial']['originating_page'] = self.request.META.get('HTTP_REFERER')
        return kwargs
