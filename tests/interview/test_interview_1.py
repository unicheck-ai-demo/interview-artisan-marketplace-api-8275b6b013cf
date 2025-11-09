import pytest
from django.urls import reverse

from app.models import Product, Vendor

pytestmark = pytest.mark.django_db


@pytest.fixture
def vendor(user):
    return Vendor.objects.create(
        user=user,
        name='Test Vendor',
        contact_email='vendor@test.com',
        description='A vendor for testing.',
    )


@pytest.fixture
def product(vendor):
    return Product.objects.create(
        vendor=vendor,
        name='Test Product',
        price=10.00,
        quantity=100,
        category='Testing',
        description='A product for testing.',
    )


@pytest.mark.xfail(strict=True)
def test_cart_quantity_accumulates(authenticated_api_client, product):
    url = reverse('api:cart')
    resp = authenticated_api_client.post(url, {'product_id': product.id, 'quantity': 2})
    assert resp.status_code == 200
    assert resp.data[str(product.id)]['quantity'] == 2

    resp = authenticated_api_client.post(url, {'product_id': product.id, 'quantity': 3})
    assert resp.status_code == 200

    resp_get = authenticated_api_client.get(url)
    assert resp_get.status_code == 200
    assert str(product.id) in resp_get.data
    assert resp_get.data[str(product.id)]['quantity'] == 5
