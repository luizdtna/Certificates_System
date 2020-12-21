from django.contrib import admin

from .models import Person, Certificate, CustomUser
# Register your models here.

admin.site.register(Certificate)
admin.site.register(Person)
admin.site.register(CustomUser)
