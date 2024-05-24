from rest_framework import serializers
from .models import *


class ProductSerializer(serializers.ModelSerializer):
    brandName = serializers.SerializerMethodField(read_only=True)
    categoryName = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Products
        fields = (
            'id',
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


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brands
        fields = (
            'brandName',
        )


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = (
            'categoryName',
        )


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = (
            'orderDate',
            'totalAmount',
            'status',
            'userId'
        )


class OrderDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDetails
        fields = (
            'quantity',
            'price',
            'orderId',
            'productsId'
        )


class GetCartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(source='productId', read_only=True)

    class Meta:
        model = CartItems
        fields = (
            'id',
            'quantity',
            'product',
            'userId'
        )


class CartItemSerializer(serializers.ModelSerializer):
    productId = serializers.IntegerField(write_only=True)

    class Meta:
        model = CartItems
        fields = (
            'productId',
        )


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payments
        fields = (
            'paymentDate',
            'amount',
            'paymentMethod',
        )
