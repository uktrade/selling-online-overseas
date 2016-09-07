from django.contrib import admin

from .models import Type, Category, ProhibitedItem


admin.site.register(Category)
admin.site.register(Type)
admin.site.register(ProhibitedItem)
