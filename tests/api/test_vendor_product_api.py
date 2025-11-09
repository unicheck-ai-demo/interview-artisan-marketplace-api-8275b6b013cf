import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status

from app.models import Vendor

pytestmark = pytest.mark.django_db
User = get_user_model()


@pytest.fixture
def vendor_user(db):
    return User.objects.create_user(username='vendorapi', password='pass')


@pytest.fixture
def authenticated_client(api_client, vendor_user):
    api_client.force_authenticate(vendor_user)
    return api_client


def test_vendor_list_create(authenticated_client):
    url = reverse('api:vendor-list')
    response = authenticated_client.get(url)
    assert response.status_code in [status.HTTP_200_OK, status.HTTP_204_NO_CONTENT]

    # Create
    data = {
        'name': 'Stone Arts',
        'description': 'Stone artisan vendor',
        'contact_email': 'stone@artisan.com',
        'phone': '12345',
    }
    response = authenticated_client.post(url, data)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['name'] == 'Stone Arts'
    assert response.data['user'] == authenticated_client.handler._force_user.id


def test_product_list_create(authenticated_client):
    # First create a vendor via service to have vendor id
    vendor = Vendor.objects.create(
        user=authenticated_client.handler._force_user,
        name='Fabric Works',
        contact_email='fabric@artisan.com',
        description='Cloth crafts',
    )
    url = reverse('api:product-list')
    response = authenticated_client.get(url)
    assert response.status_code in [status.HTTP_200_OK, status.HTTP_204_NO_CONTENT]
    product_data = {
        'vendor': vendor.id,
        'name': 'Wool Scarf',
        'price': '24.99',
        'quantity': 15,
        'category': 'Accessories',
        'description': 'Hand-knit scarf.',
    }
    response = authenticated_client.post(url, product_data)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['name'] == 'Wool Scarf'
    assert response.data['vendor'] == vendor.id
