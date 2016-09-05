from unittest import mock
from django.test import TestCase
from django.core.urlresolvers import reverse
from .forms import ContactForm
from .views import ContactView


initial_data = {
    'contact_name': 'Spam Eggs',
    'contact_email': 'spam@example.com',
    'content': 'testing contact form'
}


class ContactFormTests(TestCase):

    def test_form_valid(self):
        form = ContactForm()
        self.assertFalse(form.is_valid())
        form = ContactForm(initial_data, initial=initial_data)
        self.assertTrue(form.is_valid())


class ContactView(TestCase):

    def test_contact_get(self):
        response = self.client.get(reverse('contact:feedback_submit'))
        self.assertContains(response, "Feedback", status_code=200)

    @mock.patch('smtplib.SMTP.quit')
    @mock.patch('smtplib.SMTP.starttls')
    @mock.patch('smtplib.SMTP.login')
    @mock.patch('smtplib.SMTP.sendmail')
    def test_contact_post(self, quit_mock, starttle_mock, login_mock, sendmail_mock):
        return
        response = self.client.post(
            reverse('contact:feedback_submit'),
            {
                'contact_name': "name",
                'contact_email': 'test@test.com',
                'originating_page': '/',
                'content': 'This is feedback'
            })
        self.assertEqual(1, sendmail_mock.call_count)
        self.assertEqual(302, response.status_code)
