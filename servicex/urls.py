"""servicex URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path
from home import views as v
from dashboard import views as dv
from register import views as regv

#app_name = 'servicex'

urlpatterns = [
	path('',v.home_view, name="home"),
	path('dashboard/',dv.user_dashboard, name="user_dashboard"),
	path('dashboard/mechanic/',dv.mech_dashboard, name="mech_dashboard"),
	path('dashboard/employee/',dv.employee_dashboard, name="emp_dashboard"),
	path('dashboard/mechanic/earnings/',dv.mech_earnings, name="mech_earns"),
	path('dashboard/employee/earnings/',dv.employee_earnings, name="emp_earns"),
	path('dashboard/took_lease/',dv.user_took,name="user_took"),
    path('dashboard/gave_lease/',dv.user_gib,name="user_gib"),
    path('admin/', admin.site.urls),
    path('register/', regv.signup, name="signup"),
    path('login/',regv.login, name="login"),
    path('logout/',regv.logout, name="logout"),
]
