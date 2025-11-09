from rest_framework import serializers

from app.models import Product, Vendor


class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = [
            'id',
            'user',
            'name',
            'description',
            'contact_email',
            'phone',
            'location',
            'status',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']


class ProductSerializer(serializers.ModelSerializer):
    vendor = serializers.PrimaryKeyRelatedField(queryset=Vendor.objects.all())

    class Meta:
        model = Product
        fields = [
            'id',
            'vendor',
            'name',
            'description',
            'price',
            'quantity',
            'category',
            'image',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
