
from django.urls import path, include
from .views import FileFieldView, ShowCertificate
urlpatterns = [
    #path('',TemplateView.as_view(template_name='app_clientes/home.html'), name = 'home_url'),
    path('', ShowCertificate.as_view(), name='certificado_url'),
    path('uploadcertificados/', FileFieldView.as_view(), name='uploadcertificados_url'),

]