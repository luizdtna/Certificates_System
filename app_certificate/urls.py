from django.urls import path, include
from .views import FileFieldView, ShowCertificate, GestaoHome, \
    ListPeople, PersonUpdate, person_certificates, update_certificate

from django.contrib.auth import urls

urlpatterns = [
    #User
    path('certificados/', ShowCertificate.as_view(), name='certificado_url'),

    #Manager
    path('conta/', include('django.contrib.auth.urls')),
    path('', GestaoHome.as_view(), name='gestao_url'),
    path('uploadcertificados/', FileFieldView.as_view(), name='uploadcertificados_url'),
    path('pessoas/', ListPeople.as_view(), name='pessoas_url'),
    path('pessoas/<int:pk>/', PersonUpdate.as_view(), name='update_person_url'),
    path('pessoa/todoscertificados/<int:pk>/', person_certificates.as_view(), name='person_certificates_url'),
    path('pessoa/certificado/<int:pk>/', update_certificate.as_view(), name='update_certificate_url'),

]
