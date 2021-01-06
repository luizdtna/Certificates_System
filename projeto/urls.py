"""projeto URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include, re_path
from app_certificate import urls as certificates_urls
from app_management import urls as managements_url
from django.contrib.auth import views as auth_views
from app_certificate.views import My_Login
from django.views.generic.base import TemplateView
from django.views.static import serve
urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('',include(certificates_urls)),
    path('gerenciar/',include(managements_url)),
    path('problemas/',TemplateView.as_view(template_name='relatar_problemas.html'),name='problemas_url'),

    path('', My_Login.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout_url'),
    re_path(r'^uploads/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
