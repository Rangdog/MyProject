from django.urls import path

from . import views

urlpatterns = [
    path('products/', views.ProductMixinView.as_view()),
    path('product/<int:pk>/', views.ProductMixinView.as_view()),
    path('cartitem/', views.CartItemMixinView.as_view()),
    path('listcartitem/', views.CartItemListCreateAPIView.as_view()),
    path('cartitem/<int:pk>/', views.CartItemDeleteView.as_view()),
    path('cartitemincreasequantity/<int:pk>/',
         views.CaritemIncreaseQuantityView.as_view()),
    path('cartitemdecreasequantity/<int:pk>/',
         views.CaritemDecreaseQuantityView.as_view()),
    path('createorder/', views.CreateOrderView.as_view())
]
