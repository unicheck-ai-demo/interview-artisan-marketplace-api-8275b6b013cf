import pytest
from django.urls import reverse

from app.models import Product, Vendor

pytestmark = pytest.mark.django_db


@pytest.fixture
def vendor(user):
    return Vendor.objects.create(
        user=user,
        name='Wishlist Vendor',
        contact_email='wishlist@artisan.com',
    )


@pytest.fixture
def product(vendor):
    return Product.objects.create(
        vendor=vendor,
        name='Wish Product',
        price=9.99,
        quantity=10,
        category='WishCat',
        description='Product for wishlist testing.',
    )


@pytest.mark.xfail(strict=True)
def test_wishlist_add_and_get(authenticated_api_client, product):
    url = reverse('api:wishlist')
    resp = authenticated_api_client.post(url, {'product_id': product.id, 'quantity': None})
    assert resp.status_code == 200
    assert isinstance(resp.data, list)
    assert any(item['id'] == product.id for item in resp.data)


@pytest.mark.xfail(strict=True)
def test_wishlist_remove(authenticated_api_client, product):
    url = reverse('api:wishlist')
    authenticated_api_client.post(url, {'product_id': product.id, 'quantity': None})
    resp = authenticated_api_client.delete(url, {'product_id': product.id})
    assert resp.status_code == 200
    assert resp.data == []
