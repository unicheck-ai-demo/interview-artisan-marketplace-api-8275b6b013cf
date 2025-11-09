import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status

from app.models import Product, Vendor

pytestmark = pytest.mark.django_db
User = get_user_model()


@pytest.fixture
def vendor_user(db):
    return User.objects.create_user(username='cartvendor', password='pass')


@pytest.fixture
def customer_user(db):
    return User.objects.create_user(username='customeruser', password='pass')


@pytest.fixture
def vendor(vendor_user):
    return Vendor.objects.create(
        user=vendor_user, name='Bakery Shop', contact_email='bakery@artisan.com', description='Fresh bakery goods'
    )


@pytest.fixture
def product(vendor):
    return Product.objects.create(
        vendor=vendor, name='Sourdough Bread', price=5.50, quantity=15, category='Food', description='Fresh bread.'
    )


@pytest.fixture
def authenticated_customer(api_client, customer_user):
    api_client.force_authenticate(customer_user)
    return api_client


def test_cart_add_and_get(authenticated_customer, product):
    url = reverse('api:cart')
    resp = authenticated_customer.post(url, {'product_id': product.id, 'quantity': 2})
    assert resp.status_code == status.HTTP_200_OK
    assert str(product.id) in resp.data
    assert resp.data[str(product.id)]['quantity'] == 2
    resp = authenticated_customer.get(url)
    assert str(product.id) in resp.data


def test_checkout_process(authenticated_customer, product):
    cart_url = reverse('api:cart')
    checkout_url = reverse('api:checkout')
    authenticated_customer.post(cart_url, {'product_id': product.id, 'quantity': 3})
    resp = authenticated_customer.post(checkout_url)
    assert resp.status_code == 200
    assert resp.data['success']
    # Cart should be cleared
    resp_cart = authenticated_customer.get(cart_url)
    assert resp_cart.data == {}
