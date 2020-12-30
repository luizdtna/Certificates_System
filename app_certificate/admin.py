from django.contrib import admin

from .models import Person, Certificate, CustomUser
# Register your models here.

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('first_name','last_name',
                    'email')


admin.site.register(Certificate)
admin.site.register(Person)
admin.site.register(CustomUser)
