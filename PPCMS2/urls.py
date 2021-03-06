"""PPCMS2 URL Configuration

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
from django.urls import path, include, re_path
from django.views.generic import RedirectView
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('', RedirectView.as_view(url='account/login', permanent=False)),
    path('admin/', admin.site.urls),
    path('conference/', include('conference.urls')),
    path('account/', include('account.urls')),
    path('cfp/', include('cfp.urls')),
    re_path(r'^invitations/', include('invitations.urls', namespace='invitations')),

]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# if the DEBUG flag is true, then serve files. I need to serve these files using my webserver in production env.
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )

