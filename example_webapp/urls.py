"""example_webapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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
from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from dashboard.views import dashboard_view, car_view, mechanic_view, home_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('user_registration_bs4.urls')),
    path('', include('user_profile.urls')),
    path('', include('webpages.urls')),
    path('dashboard/',dashboard_view, name="dashboard"),
    # path('',home_view, name="home"),
    path('car/',car_view, name="car"),
    path('mechanic/',mechanic_view, name="mechanic"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
