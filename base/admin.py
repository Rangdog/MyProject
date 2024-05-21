from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Brands)
admin.site.register(Categories)
admin.site.register(Orders)
admin.site.register(Products)
admin.site.register(OrderDetails)
admin.site.register(CartItems)
admin.site.register(Payments)
