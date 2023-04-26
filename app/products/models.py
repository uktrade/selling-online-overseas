from django.db import models


class Type(models.Model):
    name = models.CharField(max_length=200, unique=True)
    sort_order = models.IntegerField()

    def __str__(self):
        return '{0}'.format(self.name)

    class Meta:
        ordering = ('sort_order',)


class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return '{0}'.format(self.name)

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Categories'


# XXX: This entire model should be removed, but doing so BREAKS migrations, so need to leave it in for now
class ProhibitedItem(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return '{0}'.format(self.name)

    class Meta:
        ordering = ('name',)
