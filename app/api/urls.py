from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CartView, CheckoutView, HealthCheckView, ProductViewSet, VendorViewSet

router = DefaultRouter()
router.register(r'vendors', VendorViewSet, basename='vendor')
router.register(r'products', ProductViewSet, basename='product')

urlpatterns = [
    path('', include(router.urls)),
    path('cart/', CartView.as_view(), name='cart'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('health/', HealthCheckView.as_view(), name='health-check'),
]

app_name = 'api'
