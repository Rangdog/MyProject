from django.shortcuts import render

from rest_framework import generics, mixins, permissions, status
from .serializers import *
from .models import *
from rest_framework.permissions import IsAuthenticated
from knox.auth import TokenAuthentication
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django.db.transaction import atomic, set_rollback
# Create your views here.


def product_exists_in_cart(product_id, user_id):
    print(user_id)
    return CartItems.objects.filter(userId__id=user_id, productId__id=product_id).exists()


class ProductMixinView(mixins.ListModelMixin, mixins.RetrieveModelMixin, generics.GenericAPIView):
    permissions_classes = [permissions.AllowAny]
    queryset = Products.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'

    def get(self, request, *args, **kwargs):
        print(args, kwargs)
        pk = kwargs.get('pk')
        if pk is not None:
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)


class CartItemListCreateAPIView(generics.ListCreateAPIView):
    queryset = CartItems.objects.all()
    serializer_class = GetCartItemSerializer
    permissions_classes = [permissions.AllowAny]

    def get_queryset(self):
        result = None
        try:
            userId = CustomeUser.objects.get(pk=self.request.user.id)
            result = CartItems.objects.filter(userId=userId)
        except:
            pass
        return result


class CartItemMixinView(generics.GenericAPIView, mixins.CreateModelMixin):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = CartItems.objects.all()
    serializer_class = CartItemSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            productId = serializer.validated_data.get('productId')
            product = Products.objects.get(pk=productId)
            userId = CustomeUser.objects.get(pk=request.user.id)
            if product_exists_in_cart(productId, request.user.id):
                cart_item = CartItems.objects.get(
                    userId=userId, productId=product)
                cart_item.quantity += 1
                cart_item.save()
            else:
                cart_item = CartItems.objects.create(
                    userId=userId, productId=product, quantity=1)
            cart_item_serializer = GetCartItemSerializer(cart_item)
            return Response(cart_item_serializer.data, status=201)


class CartItemDeleteView(generics.DestroyAPIView):
    queryset = CartItems.objects.all()
    serializer_class = GetCartItemSerializer


class CaritemIncreaseQuantityView(generics.UpdateAPIView):
    queryset = CartItems.objects.all()
    serializer_class = GetCartItemSerializer
    lookup_field = 'pk'

    def perform_update(self, serializer):
        instance = serializer.instance
        instance.quantity += 1
        instance.save()


class CaritemDecreaseQuantityView(generics.UpdateAPIView):
    queryset = CartItems.objects.all()
    serializer_class = GetCartItemSerializer
    lookup_field = 'pk'

    def perform_update(self, serializer):
        instance = serializer.instance
        if (instance.quantity > 1):
            instance.quantity -= 1
            instance.save()
        else:
            raise ValidationError("Không thể giảm hơn 1")


class CreateOrderView(generics.GenericAPIView):
    @atomic
    def post(self, request, *args, **kwargs):
        data = request.data
        address = data.get('address', "")
        number = data.get('number', "")
        total = data.get('total', 0)
        list_products = data.get('product', None)
        payment_method = data.get('paymentMethod', 0)
        try:
            order = Orders.objects.create(
                userId=CustomeUser.objects.get(pk=request.user.id),
                totalAmount=total,
                status="Chờ xác nhận",
                address=address,
                number=number,
            )
            Payments.objects.create(
                orderId=order, amount=total, paymentMethod=payment_method)
            for i in list_products:
                OrderDetails.objects.create(
                    orderId=order,
                    productsId=Products.objects.get(pk=i['product']['id']),
                    quantity=i['quantity'],
                    price=float(i['quantity']) * float(i['product']['price'])
                )
            CartItems.objects.filter(
                userId=CustomeUser.objects.get(pk=request.user.id)).delete()
            return Response("Thành công", status=status.HTTP_200_OK)
        except Exception as e:
            set_rollback(True)
            print(e)
            return Response(f"Lỗi: {e}", status=status.HTTP_400_BAD_REQUEST)
