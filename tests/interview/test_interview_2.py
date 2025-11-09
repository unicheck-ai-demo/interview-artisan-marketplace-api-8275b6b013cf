import pytest
from django.contrib.auth import get_user_model
from django.db.models.query import QuerySet

from app.services import ProductService, VendorService

pytestmark = pytest.mark.django_db


@pytest.fixture
def user(db):
    User = get_user_model()
    return User.objects.create_user(username='filtervendor', password='pass')


@pytest.fixture
def vendor(user):
    return VendorService.create_vendor(
        user=user,
        name='FilterTest Vendor',
        contact_email='filtertest@artisan.com',
        description='Vendor for filter performance tests.',
    )


@pytest.fixture
def products(vendor):
    p1 = ProductService.create_product(
        vendor=vendor,
        name='Alpha Item',
        price=10.00,
        quantity=5,
        category='TestCat',
        description='First item with category.',
    )
    p2 = ProductService.create_product(
        vendor=vendor,
        name='Beta Item',
        price=12.00,
        quantity=3,
        category='TestCat',
        description='Second item with category.',
    )
    p3 = ProductService.create_product(
        vendor=vendor,
        name='Gamma Item',
        price=15.00,
        quantity=2,
        category='OtherCat',
        description='Third item with other category.',
    )
    return p1, p2, p3


@pytest.mark.xfail(strict=True)
def test_filter_products_returns_queryset_and_filters_category(products):
    p1, p2, p3 = products
    qs = ProductService.filter_products(category='TestCat')
    assert isinstance(qs, QuerySet)
    ids = {p.id for p in qs}
    assert ids == {p1.id, p2.id}
