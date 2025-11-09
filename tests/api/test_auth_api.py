import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status

pytestmark = pytest.mark.django_db
User = get_user_model()


def test_vendor_post_requires_auth(api_client):
    url = reverse('api:vendor-list')
    data = {
        'name': 'Maple Woodcraft',
        'description': 'Handmade items',
        'contact_email': 'maple@artisan.com',
        'phone': '999-9999',
    }
    resp = api_client.post(url, data)
    assert resp.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.fixture
def vendor_user(db):
    return User.objects.create_user(username='authvendor', password='pass')


def test_cart_post_requires_auth(api_client, vendor_user):
    from app.models import Product, Vendor

    vendor = Vendor.objects.create(
        user=vendor_user,
        name='TestVendor',
        contact_email='vendor@artisan.com',
    )
    product = Product.objects.create(vendor=vendor, name='DemoProduct', price=12.34, quantity=8, category='Demo')
    url = reverse('api:cart')
    resp = api_client.post(url, {'product_id': product.id, 'quantity': 1})
    assert resp.status_code == status.HTTP_401_UNAUTHORIZED
