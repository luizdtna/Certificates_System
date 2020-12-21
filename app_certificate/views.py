from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, resolve_url
from django.views import View
from django.views.generic import FormView
import csv
from pyexcel_io import get_data
import pprint

from projeto import settings
from .models import Certificate, CustomUser
from .forms import NewCertificatesForm
# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView


class My_Login(LoginView):

    def get_success_url(self):
        if self.request.user.is_staff:
            url = resolve_url('uploadcertificados_url')
        else:
            url = self.get_redirect_url()
        return url or resolve_url(settings.LOGIN_REDIRECT_URL)


def my_view(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        # Redirect to a success page.
        ...
    else:
        # Return an 'invalid login' error message.
        ...
class FileFieldView(FormView):
    form_class = NewCertificatesForm
    template_name = 'app_certificate/upload.html'  # Replace with your template.
    success_url = '...'  # Replace with your URL or reverse().

    def list_to_vector(self):
        dados = []
        nomes = []
        emails = []
        f = open("statics/people_list.txt", "r")
        for line in f:
            #pega as linhas do arquivo, e remove o \n
            line = line.rstrip('\n')
            #divide a string em duas tabelas, uma com o nome e outra com o email
            line = line.split(';')
            nomes.append(line[0])
            emails.append(line[1])
        #dados.append(nome)
        #dados.append(email)
        return nomes, emails

    def writeListPeople(self, people):
        #A planilha é enviada para ua lista.txt em statics

        with open('statics/people_list.txt', 'wb+', ) as destination:
            for chunk in people.chunks():
                destination.write(chunk)
        nomes, email = self.list_to_vector()
        return nomes, email

    def data_isValid(self, nomes,emails,certificados):
        #Se o tamanho em caracteres for o mesmo, quer dizer que os arquivos são correspondentes
        erro = ''
        if len(nomes) == len(emails) == len(certificados):
            return True
        else:
            erro += 'ERRO: Algum arquivo(lista das pessoas ou a relação de certificados)' \
                   ' tem mais registros que o outro. Verifique se os arquivos são correspondente.'
            return erro

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        certificates = request.FILES.getlist('certificates')
        people = request.FILES['people']

        if form.is_valid():

            nomes, emails = self.writeListPeople(people)
            result = self.data_isValid(nomes, emails, certificates)
            if result == True:

                for e, n, f in zip(nomes, emails, certificates):

                    person =CustomUser.objects.filter(email=e)[0]
                    if not person:
                        person = CustomUser.objects.create_user(email=e,password='321321',first_name=n, last_name='')
                        person.save()

                    new_certificate = Certificate(certificateTitle=form.data['certificateTitle'],certificate=f,date=form.data['date'],user=person)
                    new_certificate.save()

                    #filetest = TesteModel(fileTest=f)
                    #filetest.save()
            else:
                erros = [result]
                render(request,'app_certificate/erros.html',{'erros': erros})
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

class ShowCertificate(LoginRequiredMixin,View):


    #https://docs.djangoproject.com/en/3.1/ref/forms/api/#binding-uploaded-files
#https://docs.djangoproject.com/en/3.1/topics/http/file-uploads/
#https://docs.djangoproject.com/en/3.1/topics/files/
#https://docs.djangoproject.com/en/3.1/topics/forms/modelforms/#django.forms.ModelForm

    def get(self, request, *args, **kwargs):

        date = Certificate.objects.filter(user__id=request.user.id)
        if request.user.is_staff:
            pass
        return render(request,'app_certificate/show_certificate.html',{'date':date})



class RemoveCertificate(View):
    #nada = Certificate.objects.filter()
    outracoisa = Certificate._delete_file("uploads/certificates/museo3.jpg")

