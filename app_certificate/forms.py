from django import forms
from django.contrib.auth.forms import AuthenticationForm, UsernameField

CHOICES=[('ponto_virgula','ponto e virgula'),
         ('virgula','virgula')]

class CustomAuthenticationForm(AuthenticationForm):
    username = UsernameField(
        label='Email',
    )
    password = forms.CharField(
        label="senha",
        strip=False,
        widget=forms.PasswordInput,

    )

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()


class NewCertificatesForm(forms.Form):
    certificateTitle = forms.CharField(label='Titulo do certificado')
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label='Data de realização')
    people = forms.FileField(label='Lista de pessoas presentes')
    separador = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)
    certificates = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'multiple': True}), label='Certificados')

class Search_Person_Form(forms.Form):
    name = forms.CharField(label='Pesquisa por nome ou email')


