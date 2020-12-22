from django import forms

CHOICES=[('ponto_virgula','ponto e virgula'),
         ('virgula','virgula')]

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()


class NewCertificatesForm(forms.Form):
    certificateTitle = forms.CharField()
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    people = forms.FileField()
    separador = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)
    certificates = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))

