from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DestinationViewSet, TravelPlanViewSet

router = DefaultRouter()
router.register(r'destinations', DestinationViewSet)
router.register(r'plans', TravelPlanViewSet, basename='plan')

urlpatterns = [
    path('api/', include(router.urls)),
]
