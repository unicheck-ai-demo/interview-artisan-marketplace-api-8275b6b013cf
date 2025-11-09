from decimal import Decimal

import pytest
from django.contrib.auth import get_user_model

from app.services import ProductService, VendorService

pytestmark = pytest.mark.django_db
User = get_user_model()


def test_vendor_service_create_and_get():
    user = User.objects.create_user(username='vendoruser1', password='pass')
    vendor = VendorService.create_vendor(
        user=user,
        name='Glass Art',
        contact_email='glass@artisan.com',
        description='Modern glass work',
        phone='555-2345',
    )
    found_vendor = VendorService.get_vendor(vendor.id)
    assert found_vendor.name == vendor.name
    assert found_vendor.description == 'Modern glass work'


def test_product_service_create_and_get():
    user = User.objects.create_user(username='vendoruser2', password='pass')
    vendor = VendorService.create_vendor(
        user=user,
        name='Leatherworks',
        contact_email='leather@artisan.com',
        description='Fine leather',
        phone='555-4321',
    )
    product = ProductService.create_product(
        vendor=vendor,
        name='Leather Wallet',
        price=49.99,
        quantity=10,
        category='Accessories',
        description='Handmade leather wallet',
    )
    found_product = ProductService.get_product(product.id)
    assert found_product.name == 'Leather Wallet'
    assert found_product.vendor == vendor
    assert found_product.price == Decimal('49.99')
