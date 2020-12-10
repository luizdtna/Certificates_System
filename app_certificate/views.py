from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from .models import Certificate

# Create your views here.
class ShowCertificate(View):

#https://docs.djangoproject.com/en/3.1/ref/forms/api/#binding-uploaded-files
#https://docs.djangoproject.com/en/3.1/topics/http/file-uploads/
#https://docs.djangoproject.com/en/3.1/topics/files/
#https://docs.djangoproject.com/en/3.1/topics/forms/modelforms/#django.forms.ModelForm
    def get(self, request, *args, **kwargs):
        date = Certificate.objects.filter(person__id=kwargs['pk'])

        return render(request,'certificates/show_certificate.html',{'date':date})



class RemoveCertificate(View):
    #nada = Certificate.objects.filter()
    outracoisa = Certificate._delete_file("uploads/certificates/museo3.jpg")