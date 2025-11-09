from django.contrib.auth import get_user_model

from app.models import Product, Vendor

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
