from django.db import models

from login.models import *

# Create your models here.


class Brands(models.Model):
    brandName = models.CharField(max_length=256)


class Categories(models.Model):
    categoryName = models.CharField(max_length=256)


class Orders(models.Model):
    userId = models.ForeignKey(CustomeUser, on_delete=models.CASCADE)
    orderDate = models.DateTimeField(auto_now_add=True)
    totalAmount = models.DecimalField(
        max_digits=20, decimal_places=2, default=0)
    status = models.CharField(max_length=20)


class Products(models.Model):
    productName = models.CharField(max_length=256)
    size = models.CharField(max_length=5)
    color = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    stockQuantity = models.DecimalField(max_digits=20)
    description = models.CharField()
    imgURL = models.URLField()
    brandId = models.ForeignKey(Brands, on_delete=models.CASCADE)
    categoryId = models.ForeignKey(Categories, on_delete=models.CASCADE)


class OrderDetails(models.Model):
    orderId = models.ForeignKey(Orders, on_delete=models.CASCADE)
    productsId = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=20)
    price = models.DecimalField(max_digits=20, decimal_places=2)


class CartItems(models.Model):
    quantity = models.DecimalField(max_digits=20)
    userId = models.ForeignKey()
