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
    path('map/',regv.map, name="map"),
    path('get_loc/',regv.get_loc, name="get_loc"),
    path('update_loc/',regv.update_loc,name="update_loc"),
    path('car_details_of/<str:email>/',dv.car_details,name="car_details"),
    path('mech_details_of/<str:email>/',dv.mech_details,name="mech_details"),
    path('checkout/',dv.checkout_view, name = "checkout"),
    path('tandc/',dv.tandc, name = "tandc"),
    path('mech_checkout/',dv.mech_checkout_view, name = "mech_checkout"),
    path('success/<str:value>/<str:email>/',dv.success_payment, name = "success"),
<<<<<<< Updated upstream

=======
    path('mechanic-booking', dv.mechanic_booking, name="mechanic_booking"),
    path('api/',include('api.urls')),
>>>>>>> Stashed changes
]
