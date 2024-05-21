from django.shortcuts import render

from rest_framework import generics, mixins, permissions
from .serializers import *
from .models import *
# Create your views here.


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
