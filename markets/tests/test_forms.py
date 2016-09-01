from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from ..forms import LogoAdminForm
from . import load_sample_png


class LogoAdminFormTests(TestCase):

    def test_file_validation(self):
        upload_file = load_sample_png()
        post_dict = {'name': 'logo'}
        file_dict = {'logo': SimpleUploadedFile(upload_file.name, upload_file.read())}
        form = LogoAdminForm(post_dict, file_dict)
        self.assertTrue(form.is_valid())

    def test_invalid_file(self):
        post_dict = {'name': 'logo'}
        file_dict = {'logo': SimpleUploadedFile("test.png", b'')}
        form = LogoAdminForm(post_dict, file_dict)
        self.assertFalse(form.is_valid())

    def test_invalid_filename(self):
        upload_file = load_sample_png()
        post_dict = {'name': 'logo'}
        file_dict = {'logo': SimpleUploadedFile("test.jpg", upload_file.read())}
        form = LogoAdminForm(post_dict, file_dict)
        self.assertFalse(form.is_valid())
