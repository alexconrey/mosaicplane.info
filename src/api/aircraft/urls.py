from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ManufacturerViewSet, AircraftViewSet

router = DefaultRouter()
router.register(r'manufacturers', ManufacturerViewSet)
router.register(r'aircraft', AircraftViewSet)

urlpatterns = [
    path('', include(router.urls)),
]