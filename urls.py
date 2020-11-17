from rest_framework import routers
from django.urls import path, include
from api.views import CarViewSet, MechanicViewSet, UserViewSet

router = routers.DefaultRouter()
router.register(r'cars', CarViewSet, basename='cars')
router.register(r'mechanic', MechanicViewSet, basename='mechanic')
router.register(r'user', UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
]