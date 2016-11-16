from django.db import models


class Region(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return "{0}".format(self.name)

    class Meta:
        ordering = ('-name',)


class Country(models.Model):
    name = models.CharField(max_length=200, unique=True)
    alternate_name = models.CharField(max_length=200, null=True, blank=True)
    region = models.ForeignKey(Region)

    def __str__(self):
        return "{0}".format(self.name)

    class Meta:
        verbose_name_plural = "Countries"
        ordering = ('-name',)
