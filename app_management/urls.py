
from django.urls import path, include

from .views import FileFieldView

urlpatterns = [

    path('uploadcertificados/',FileFieldView.as_view(), name = 'uploadcertificados_url'),


]

