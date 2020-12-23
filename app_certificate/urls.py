
from django.urls import path, include
from .views import FileFieldView, ShowCertificate, GestaoHome, \
    ListPeople, PersonUpdate,person_certificates, update_certificate
from django.views.generic.base import TemplateView

urlpatterns = [
    #path('',TemplateView.as_view(template_name='app_clientes/gestao.html'), name = 'home_url'),
    path('certificados/', ShowCertificate.as_view(), name='certificado_url'),

    path('gestao/', GestaoHome.as_view(), name='gestao_url'),
    path('gestao/uploadcertificados/', FileFieldView.as_view(), name='uploadcertificados_url'),
    path('gestao/pessoas/', ListPeople.as_view(), name='pessoas_url'),
    path('gestao/pessoas/<int:pk>/', PersonUpdate.as_view(), name='update_person_url'),
    path('gestao/pessoa/todoscertificados/<int:pk>/', person_certificates.as_view(), name='person_certificates_url'),
    path('gestao/pessoa/certificado/<int:pk>/', update_certificate.as_view(), name='update_certificate_url'),


]