
from django.urls import path, include
from .views import FileFieldView, ShowCertificate, gestao_home
from django.views.generic.base import TemplateView

urlpatterns = [
    #path('',TemplateView.as_view(template_name='app_clientes/gestao.html'), name = 'home_url'),
    path('certificados/', ShowCertificate.as_view(), name='certificado_url'),

    path('gestao/',gestao_home.as_view(), name='gestao_url'),
    path('gestao/uploadcertificados/', FileFieldView.as_view(), name='uploadcertificados_url'),

]