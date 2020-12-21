from django import forms

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()


class NewCertificatesForm(forms.Form):
    certificateTitle = forms.CharField()
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    people = forms.FileField()
    certificates = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))

