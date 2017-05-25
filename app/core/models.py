"""
These models are just for unit tests in this module.  Unfortunately, until https://code.djangoproject.com/ticket/7835
is resolved, we can't just have models that are created solely at unit test runtime.

THESE MODELS SHOULD NOT BE USED ANYWHERE IN CODE OUTSIDE OF UNIT TESTS
"""

from django.db import models


class TestModel1(models.Model):
    name = models.CharField(max_length=200)
    symbol = models.CharField(max_length=1, blank=True, null=True)

    def __str__(self):
        return "{0}".format(self.name, self.symbol)


class TestModel2(models.Model):
    name = models.CharField(max_length=200)
    other_model = models.ManyToManyField(TestModel1)

    def __str__(self):
        return "{0}".format(self.name)
