from decimal import Decimal

from django.contrib.auth import get_user_model
from django.contrib.gis.geos import Point
from django.core.cache import cache
from django.db import transaction
from django.utils import timezone

from app.models import Order, OrderItem, Product, Vendor

User = get_user_model()


class VendorService:
    @staticmethod
    def create_vendor(
        user: User, name: str, contact_email: str, description='', phone='', location=None, status='active'
    ) -> Vendor:
        vendor = Vendor.objects.create(
            user=user,
            name=name,
            contact_email=contact_email,
            description=description,
            phone=phone,
            location=location,
            status=status,
        )
        return vendor

    @staticmethod
    def get_vendor(vendor_id: int) -> Vendor:
        return Vendor.objects.select_related('user').get(id=vendor_id)

    @staticmethod
    def update_vendor(vendor: Vendor, **kwargs) -> Vendor:
        for attr, value in kwargs.items():
            if hasattr(vendor, attr):
                setattr(vendor, attr, value)
        vendor.save()
        return vendor

    @staticmethod
    def delete_vendor(vendor: Vendor) -> None:
        vendor.delete()

    @staticmethod
    def get_vendors_in_location(location: Point, radius_km: float):
        if not location:
            return Vendor.objects.none()
        return Vendor.objects.filter(location__distance_lte=(location, radius_km * 1000))


class ProductService:
    @staticmethod
    def create_product(
        vendor: Vendor, name: str, price: float, quantity: int, category: str = '', description='', image=None
    ) -> Product:
        product = Product.objects.create(
            vendor=vendor,
            name=name,
            price=price,
            quantity=quantity,
            category=category,
            description=description,
            image=image,
        )
        return product

    @staticmethod
    def get_product(product_id: int) -> Product:
        return Product.objects.select_related('vendor').get(id=product_id)

    @staticmethod
    def update_product(product: Product, **kwargs) -> Product:
        for attr, value in kwargs.items():
            if hasattr(product, attr):
                setattr(product, attr, value)
        product.save()
        return product

    @staticmethod
    def delete_product(product: Product) -> None:
        product.delete()

    @staticmethod
    def filter_products(category=None, price_min=None, price_max=None, vendor_location=None, vendor_radius_km=None):
        products = list(Product.objects.select_related('vendor').all())
        if category:
            products = [p for p in products if p.category == category]
        if price_min is not None:
            products = [p for p in products if p.price >= Decimal(price_min)]
        if price_max is not None:
            products = [p for p in products if p.price <= Decimal(price_max)]
        if vendor_location and vendor_radius_km:
            vendors = VendorService.get_vendors_in_location(vendor_location, vendor_radius_km)
            products = [p for p in products if p.vendor in vendors]
        return products


class CartService:
    CART_TTL = 3600
    REDIS_PREFIX = 'cart:'

    @staticmethod
    def _cart_key(user_id):
        return f'{CartService.REDIS_PREFIX}{user_id}'

    @staticmethod
    def get_cart(user_id):
        cart = cache.get(CartService._cart_key(user_id))
        # Ensure all quantities are integers
        if cart:
            cart_int = {str(pid): int(qty) for pid, qty in cart.items()}
            return cart_int
        return {}

    @staticmethod
    def set_cart(user_id, cart_data):
        # Ensure all quantities are integers when storing
        clean_cart = {str(pid): int(qty) for pid, qty in cart_data.items()}
        cache.set(CartService._cart_key(user_id), clean_cart, timeout=CartService.CART_TTL)

    @staticmethod
    def add_item(user_id, product_id, quantity):
        cart = CartService.get_cart(user_id)
        cart[str(product_id)] = int(quantity)
        CartService.set_cart(user_id, cart)
        return cart

    @staticmethod
    def remove_item(user_id, product_id):
        cart = CartService.get_cart(user_id)
        cart.pop(str(product_id), None)
        CartService.set_cart(user_id, cart)
        return cart

    @staticmethod
    def clear_cart(user_id):
        cache.delete(CartService._cart_key(user_id))

    @staticmethod
    def get_items(user_id):
        cart = CartService.get_cart(user_id)
        products = Product.objects.filter(id__in=cart.keys())
        return {(str(p.id)): {'product': p, 'quantity': int(cart[str(p.id)])} for p in products}


class CheckoutService:
    @staticmethod
    @transaction.atomic
    def checkout(user: User):
        cart = CartService.get_cart(user.id)
        cart_items = Product.objects.select_for_update().filter(id__in=cart.keys())
        order_map = {}
        for product in cart_items:
            qty = int(cart[str(product.id)])
            if product.quantity < qty:
                raise Exception(f'Not enough stock for product {product.name}')
            product.quantity -= qty
            product.save()
            vendor_id = product.vendor.id
            if vendor_id not in order_map:
                order_map[vendor_id] = Order.objects.create(
                    customer=user, vendor=product.vendor, status='completed', total_amount=0
                )
            OrderItem.objects.create(
                order=order_map[vendor_id], product=product, quantity=qty, unit_price=product.price
            )
            order_map[vendor_id].total_amount += product.price * qty
        for order in order_map.values():
            order.status = 'completed'
            order.completed_at = timezone.now()
            order.save()
        CartService.clear_cart(user.id)
        return [order for order in order_map.values()]


class VendorAnalyticsService:
    @staticmethod
    def sales_stats(vendor_id):
        from django.db.models import Count, Sum

        qs = Order.objects.filter(vendor_id=vendor_id, status='completed')
        total_sales = qs.aggregate(total_amount=Sum('total_amount'), total_orders=Count('id'))
        return total_sales
