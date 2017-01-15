"""smogtrac URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from webui import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^rest/refresh/start/(?P<area>[A-Za-z\ ąćęłóśżźĄĆĘŁÓŚŻŹ]+)/(?P<pm_type>[A-Za-z0-9\.\-]+)$', views.startDataRefresh, name='start_refresh'),
    url(r'^rest/refresh/check$', views.checkDataRefresh, name='check_refresh'),
    url(r'^admin/', admin.site.urls),
]
