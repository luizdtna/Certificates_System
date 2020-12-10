from django.contrib import admin

from .models import Person, Certificate
# Register your models here.

admin.site.register(Certificate)
admin.site.register(Person)