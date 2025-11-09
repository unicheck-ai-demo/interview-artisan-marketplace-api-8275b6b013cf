from django.contrib.gis.geos import Point
from django.db import DatabaseError, connection
from rest_framework import status, views, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from app.api.serializers import ProductSerializer, VendorSerializer
from app.models import Product, Vendor
from app.services import CartService, CheckoutService, ProductService, VendorAnalyticsService


class HealthCheckView(APIView):
    def get(self, request):
        try:
            with connection.cursor() as cursor:
                cursor.execute('SELECT PostGIS_Full_Version();')
                cursor.fetchone()
        except DatabaseError as e:
            return Response({'status': 'error', 'db': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({'status': 'ok'}, status=status.HTTP_200_OK)


class VendorViewSet(viewsets.ModelViewSet):
    queryset = Vendor.objects.select_related('user').all()
    serializer_class = VendorSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated])
    def analytics(self, request, pk=None):
        stats = VendorAnalyticsService.sales_stats(pk)
        return Response(stats)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.select_related('vendor').all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.query_params.get('category')
        price_min = self.request.query_params.get('price_min')
        price_max = self.request.query_params.get('price_max')
        lat = self.request.query_params.get('lat')
        lng = self.request.query_params.get('lng')
        radius_km = self.request.query_params.get('radius_km')
        vendor_location = None
        if lat and lng:
            try:
                vendor_location = Point(float(lng), float(lat))
            except Exception:
                vendor_location = None
        return (
            ProductService.filter_products(
                category=category,
                price_min=price_min,
                price_max=price_max,
                vendor_location=vendor_location,
                vendor_radius_km=float(radius_km) if radius_km else None,
            )
            if (category or price_min or price_max or vendor_location)
            else queryset
        )


class CartView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart = CartService.get_items(request.user.id)
        resp = {}
        for pid, item in cart.items():
            prod = item['product']
            resp[pid] = {'name': prod.name, 'quantity': item['quantity'], 'price': str(prod.price)}
        return Response(resp)

    def post(self, request):
        pid = request.data.get('product_id')
        qty = request.data.get('quantity')
        CartService.add_item(request.user.id, pid, qty)
        return self.get(request)

    def delete(self, request):
        pid = request.data.get('product_id')
        CartService.remove_item(request.user.id, pid)
        return self.get(request)


class CheckoutView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            orders = CheckoutService.checkout(request.user)
            return Response({'success': True, 'orders': [o.id for o in orders]})
        except Exception as e:
            return Response({'success': False, 'error': str(e)}, status=400)
