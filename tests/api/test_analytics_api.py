import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status

from app.models import Order, OrderItem, Product, Vendor

pytestmark = pytest.mark.django_db
User = get_user_model()


@pytest.fixture
def vendor_user(db):
    return User.objects.create_user(username='statsvendor', password='pass')


@pytest.fixture
def customer_user(db):
    return User.objects.create_user(username='statscustomer', password='pass')


@pytest.fixture
def vendor(vendor_user):
    return Vendor.objects.create(
        user=vendor_user,
        name='StatVendor',
        contact_email='stats@artisan.com',
    )


@pytest.fixture
def authenticated_client(api_client, vendor_user):
    api_client.force_authenticate(vendor_user)
    return api_client


@pytest.fixture
def completed_order(vendor, customer_user):
    # Create and mark completed order
    product = Product.objects.create(vendor=vendor, name='StatProduct', price=10.00, quantity=50, category='TestCat')
    order = Order.objects.create(
        customer=customer_user,
        vendor=vendor,
        status='completed',
        total_amount=20.00,
    )
    OrderItem.objects.create(order=order, product=product, quantity=2, unit_price=10.00)
    return order


def test_vendor_analytics(authenticated_client, vendor, completed_order):
    url = reverse('api:vendor-analytics', args=[vendor.id])
    resp = authenticated_client.get(url)
    assert resp.status_code == status.HTTP_200_OK
    stats = resp.data
    assert stats['total_orders'] == 1
    assert float(stats['total_amount']) == 20.00
