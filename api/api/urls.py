from rest_framework import routers
from django.urls import path, include
from api.views import CarViewSet, MechanicViewSet, UserViewSet
from django.conf.urls import url 
from api import views 

router = routers.DefaultRouter()
router.register(r'car', CarViewSet, basename='cars')
router.register(r'mechanic', MechanicViewSet, basename='mechanic')
router.register(r'user', UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
    path('cars/',views.carGP.as_view()),
    path('cars/<str:pk>',views.carGDU.as_view()),
    path('mechs/',views.mechGP.as_view()),
    path('mechs/<str:pk>',views.mechGDU.as_view()),
    path('users/',views.userGP.as_view()),
    path('users/<str:pk>',views.userGDU.as_view()),
    path('emps/',views.employeeGP.as_view()),
    path('emps/<str:pk>',views.employeeGDU.as_view()),
    path('cbookings/',views.cBookingGP.as_view()),
    path('cbookings/<str:pk>',views.cBookingGDU.as_view()),
    path('mbookings/',views.mBookingGP.as_view()),
    path('mbookings/<str:pk>',views.mBookingGDU.as_view()),
    path('verifications/',views.verGP.as_view()),
    path('verifications/<str:pk>',views.verGDU.as_view()),
]
