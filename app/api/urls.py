from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import HealthCheckView, ProductViewSet, VendorViewSet

router = DefaultRouter()
router.register(r'vendors', VendorViewSet, basename='vendor')
router.register(r'products', ProductViewSet, basename='product')

urlpatterns = [
    path('', include(router.urls)),
    path('health/', HealthCheckView.as_view(), name='health-check'),
]

app_name = 'api'
