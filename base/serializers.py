from rest_framework import serializers
from .models import *


class ProductSerializer(serializers.ModelSerializer):
    brandName = serializers.SerializerMethodField(read_only=True)
    categoryName = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Products
        fields = (
            'productName',
            'size',
            'color',
            'price',
            'stockQuantity',
            'description',
            'imgURL',
            'brandName',
            'categoryName'
        )

    def get_brandName(self, obj):
        try:
            return obj.brandId.brandName
        except:
            return None

    def get_categoryName(self, obj):
        try:
            return obj.categoryId.categoryName
        except:
            return None
