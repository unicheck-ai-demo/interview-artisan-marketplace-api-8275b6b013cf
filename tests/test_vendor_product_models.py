import pytest
from django.contrib.auth import get_user_model

from app.models import Product, Vendor

pytestmark = pytest.mark.django_db

User = get_user_model()


def test_vendor_creation():
    user = User.objects.create_user(username='vendoruser', password='pass')
    vendor = Vendor.objects.create(
        user=user,
        name='Handcrafts by Alice',
        contact_email='alice@artisan.com',
        description='Alice makes pottery.',
        phone='123-123-1234',
    )
    assert vendor.id is not None
    assert vendor.name == 'Handcrafts by Alice'
    assert vendor.user.username == 'vendoruser'


def test_product_creation():
    user = User.objects.create_user(username='vendor2', password='pass')
    vendor = Vendor.objects.create(
        user=user,
        name='Woodwork Wonders',
        contact_email='bob@artisan.com',
        description='Fine woodwork.',
        phone='555-555-5555',
    )
    product = Product.objects.create(
        vendor=vendor,
        name='Oak Table',
        price=299.99,
        quantity=5,
        category='Furniture',
    )
    assert product.id is not None
    assert product.vendor == vendor
    assert product.price == 299.99
    assert product.name == 'Oak Table'
