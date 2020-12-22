import re

from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, resolve_url, redirect
from django.urls import reverse_lazy
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

class gestao_home(LoginRequiredMixin, View):

    def get(self, request):
        return render(request,'app_certificate/gestao.html')

class FileFieldView(LoginRequiredMixin,FormView):

    form_class = NewCertificatesForm
    template_name = 'app_certificate/upload.html'  # Replace with your template.
    success_url = reverse_lazy('uploadcertificados_url')  # Replace with your URL or reverse().

    def form_valid(self, form):
        """If the form is valid, redirect to the supplied URL."""
        return self.render_to_response({'form':form, 'success':True})

    def list_to_vector(self, separator):
        dados = []
        nomes = []
        emails = []
        f = open("statics/people_list.txt", "r")
        for line in f:
            #pega as linhas do arquivo, e remove o \n
            line = line.rstrip('\n')
            #divide a string em duas tabelas, uma com o nome e outra com o email
            if separator == 'ponto_virgula':
                line = line.split(';')
            else:
                #separator is ','
                line = line.split(',')
            nomes.append(line[0])
            emails.append(line[1])
        #dados.append(nome)
        #dados.append(email)

        emails_aux = []
        #passando emails para minusculo
        for email in emails:
            emails_aux.append(email.lower())

        return nomes, emails_aux

    def writeListPeople(self, people):
        #A planilha é enviada para ua lista.txt em statics

        with open('statics/people_list.txt', 'wb+', ) as destination:
            for chunk in people.chunks():
                destination.write(chunk)

    def filterEmails(self, emails):
        #Verifica se é um email válido
        r = re.compile(r'^[a-zA-Z0-9._-]+@(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}$')
        #filtered_emails = [email for email in emails if r.match(email)]
        for email in emails:
            if not r.match(email):
                return False
        return True

    def filterNames(self, names):
        # Verifica se o campo nome está vazio
        for name in names:
            if name == '':
                return False
        return True

    def data_isValid(self, nomes,emails,certificados):
        #Se o tamanho em caracteres for o mesmo, quer dizer que os arquivos são correspondentes
        erro = ''
        # If the every registers have the same length
        if len(nomes) == len(emails) == len(certificados):
            result_0 = self.filterEmails(emails)
            result_1 = self.filterNames(nomes)
            if result_0 == False:
                erro +='ERRO: Existe um ou mais registros na coluna de Emails incorretos'
                return erro
            elif result_1 == False:
                erro += 'ERRO: Existe um ou mais registros na coluna de Nomes invalidos'
                return erro
            else:
                # Every registers are right
                return True
        else:
            erro += 'ERRO: Algum arquivo(lista das pessoas ou a relação de certificados)' \
                   ' tem mais registros que o outro. Verifique se os arquivos são correspondente.\n'
            return erro

    def get(self, request, *args, **kwargs):
        if not request.user.is_staff:
            # Se o usuário não for staff, ele não pode acessar essa view
            return redirect('certificado_url')
        else:
            return render(request,'app_certificate/upload.html',{'form':self.form_class})


    def post(self, request, *args, **kwargs):

        form_class = self.get_form_class()
        form = self.get_form(form_class)
        certificates = request.FILES.getlist('certificates')
        people = request.FILES['people']

        result = ''
        if form.is_valid():
            try:
                self.writeListPeople(people)
                nomes, emails = self.list_to_vector(request.POST['separador'])
                result = self.data_isValid(nomes, emails, certificates)
            except IndexError:
                result += 'ERRO: Selecione o separador correto(virgula ou ponto e virgula)\n'

            if result == True:

                for n, e, f in zip(nomes, emails, certificates):

                    try:
                        person = CustomUser.objects.get(email=e)
                    except CustomUser.DoesNotExist:
                        #If there's not this person
                        person = CustomUser.objects.create_user(email=e, password='321321', first_name=n, last_name='')
                        person.save()

                    new_certificate = Certificate(certificateTitle=form.data['certificateTitle'],certificate=f,date=form.data['date'],user=person)
                    new_certificate.save()

                    #filetest = TesteModel(fileTest=f)
                    #filetest.save()
            else:
                erros = [result]
                print('here')
                return render(request,'app_certificate/erros.html',{'erros': erros})
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

