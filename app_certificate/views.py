import re

from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, resolve_url, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView, UpdateView
from django.contrib import messages
from projeto import settings
from .models import Certificate, CustomUser
from .forms import NewCertificatesForm, CustomAuthenticationForm, Search_Person_Form
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.db.models import Q


# Create your views here.


class My_Login(LoginView):
    authentication_form = CustomAuthenticationForm

    def get_success_url(self):

        if self.request.user.is_staff:
            url = resolve_url('gestao_url')
            return url
        else:
            return super(My_Login, self).get_success_url()


class GestaoHome(LoginRequiredMixin, View):

    def get(self, request):
        if request.user.is_staff:
            return render(request, 'app_certificate/gestao.html')
        else:
            return redirect('certificado_url')


class FileFieldView(LoginRequiredMixin, FormView):
    form_class = NewCertificatesForm
    template_name = 'app_certificate/upload.html'  # Replace with your template.
    success_url = reverse_lazy('uploadcertificados_url')  # Replace with your URL or reverse().

    def form_valid(self, form):
        """If the form is valid, redirect to the supplied URL."""
        return self.render_to_response({'form': form, 'success': True})

    def list_to_vector(self, separator):
        dados = []
        nomes = []
        emails = []
        f = open("statics/people_list.txt", "r")
        for line in f:
            # pega as linhas do arquivo, e remove o \n
            line = line.rstrip('\n')
            # divide a string em duas tabelas, uma com o nome e outra com o email
            if separator == 'ponto_virgula':
                line = line.split(';')
            else:
                # separator is ','
                line = line.split(',')
            nomes.append(line[0])
            emails.append(line[1])
        # dados.append(nome)
        # dados.append(email)

        emails_aux = []
        # passando emails para minusculo
        for email in emails:
            emails_aux.append(email.lower())

        return nomes, emails_aux

    def writeListPeople(self, people):
        # A planilha é enviada para ua lista.txt em statics
        aux_is_csv = str(people)
        if aux_is_csv[-4:] == '.csv':
            with open('statics/people_list.txt', 'wb+', ) as destination:
                for chunk in people.chunks():
                    destination.write(chunk)
            return True
        return False

    def filterEmails(self, emails):
        # Verifica se é um email válido
        r = re.compile(r'^[a-zA-Z0-9._-]+@(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}$')
        # filtered_emails = [email for email in emails if r.match(email)]
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

    def data_isValid(self, nomes, emails, certificados):
        # Se o tamanho em caracteres for o mesmo, quer dizer que os arquivos são correspondentes
        erro = ''
        # If the every registers have the same length
        if len(nomes) == len(emails) == len(certificados):
            result_0 = self.filterEmails(emails)
            result_1 = self.filterNames(nomes)
            if result_0 == False:
                erro += 'ERRO: Existe um ou mais registros na coluna de Emails incorretos'
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
        if request.user.is_staff:
            aux = super(FileFieldView, self).get(request, *args, **kwargs)
            return aux
        else:
            # Se o usuário não for staff, ele não pode acessar essa view
            return redirect('certificado_url')

    def post(self, request, *args, **kwargs):

        global nomes, emails
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        certificates = request.FILES.getlist('certificates')
        people = request.FILES['people']

        result = ''
        if form.is_valid():
            try:
                is_valid = self.writeListPeople(people)
                if is_valid:
                    nomes, emails = self.list_to_vector(request.POST['separador'])
                    result = self.data_isValid(nomes, emails, certificates)
                else:
                    result += 'ERRO: O arquivo de pessoas tem o formato inválido, ' \
                              'é necessário o formato .csv'
            except IndexError:
                result += 'ERRO: Selecione o separador correto(virgula ou ponto e virgula)\n'

            if result == True:

                for n, e, f in zip(nomes, emails, certificates):

                    try:
                        person = CustomUser.objects.get(email=e)
                    except CustomUser.DoesNotExist:
                        # If there's not this person
                        person = CustomUser.objects.create_user(email=e, password='321321', first_name=n, last_name='')
                        person.save()

                    new_certificate = Certificate(certificateTitle=form.data['certificateTitle'], certificate=f,
                                                  date=form.data['date'], user=person)
                    new_certificate.save()

                    # filetest = TesteModel(fileTest=f)
                    # filetest.save()
            else:
                erros = [result]
                print('here')
                return render(request, 'app_certificate/erros.html', {'erros': erros})
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class ShowCertificate(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        date = Certificate.objects.filter(user__id=request.user.id).order_by('date')
        if request.user.is_staff:
            pass
        return render(request, 'app_certificate/show_certificate.html', {'date': date})


class ListPeople(LoginRequiredMixin, ListView):
    model = CustomUser
    template_name = 'app_certificate/people_list.html'
    search_person_form = Search_Person_Form
    ordering = 'first_name' # Ordenação da Queryset

    def get(self, request, *args, **kwargs):
        if request.user.is_staff:
            aux = super(ListPeople, self).get(request, args, kwargs)
            return aux
        else:
            return redirect('certificado_url')

    def get_context_data(self, **kwargs):
        context = super(ListPeople, self).get_context_data(**kwargs)
        context['form'] = self.search_person_form
        return context

    def post(self, request):
        form = self.search_person_form(self.request.POST)
        if form.is_valid():
            # filtra por nome OU email
            list = CustomUser.objects.filter(
                Q(first_name__contains=request.POST['name']) | Q(email=request.POST['name']))
            context = self.get_context_data(object_list=list)
        return render(request, self.template_name, context)


class PersonUpdate(LoginRequiredMixin, UpdateView):
    model = CustomUser
    fields = ['first_name', 'last_name', 'email']
    template_name = 'app_certificate/person_update.html'
    success_url = reverse_lazy('pessoas_url')

    def get(self, request, *args, **kwargs):
        if request.user.is_staff:
            aux = super(PersonUpdate, self).get(request, args, kwargs)
            return aux
        else:
            return redirect('certificado_url')

    def form_valid(self, form):
        messages.success(self.request, "Os dados foram atualizados com sucesso!")

        super().form_valid(form)
        return HttpResponseRedirect(self.get_success_url())


class RemoveCertificate(LoginRequiredMixin, View):
    # nada = Certificate.objects.filter()
    outracoisa = Certificate._delete_file("uploads/certificates/museo3.jpg")


class person_certificates(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):

        if request.user.is_staff:
            certificates = Certificate.objects.filter(user__pk=kwargs['pk']).order_by('date')
            user = CustomUser.objects.get(pk=kwargs['pk'])
            return render(request, 'app_certificate/person_certificates.html',
                          {'certificates': certificates, 'user': user})
        else:
            # Se o usuário não for staff, ele não pode acessar essa view
            return redirect('certificado_url')


class update_certificate(LoginRequiredMixin, UpdateView):
    # TODO: Precisarei trocar mudar a forma que os dados são atualizados, isso porque o arquivo não é sobrescrito
    #  pelo novo, ficando o lixo armazenado.
    model = Certificate
    fields = ['certificate', 'date', 'certificateTitle']
    template_name = 'app_certificate/update_certificate.html'
    success_url = reverse_lazy('pessoas_url')

    def get(self, request, *args, **kwargs):
        if request.user.is_staff:
            aux = super(update_certificate, self).get(request, args, kwargs)
            return aux
        else:
            return redirect('certificado_url')

    def form_valid(self, form):
        messages.success(self.request, "Os dados foram atualizados com sucesso!")

        super().form_valid(form)
        return HttpResponseRedirect(self.get_success_url())
