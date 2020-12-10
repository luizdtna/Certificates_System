from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import UploadFileForm, FileFieldForm
from django.views.generic.edit import FormView
from .models import TesteModel
# Imaginary function to handle an uploaded file.
#from somewhere import handle_uploaded_file

class FileFieldView(FormView):
    form_class = FileFieldForm
    template_name = 'upload2.html'  # Replace with your template.
    success_url = '...'  # Replace with your URL or reverse().

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        files = request.FILES.getlist('file_field')
        if form.is_valid():
            for f in files:
                filetest = TesteModel(fileTest=f)
                filetest.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

