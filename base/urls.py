from django.urls import path

from . import views

urlpatterns = [
    path('products/', views.ProductMixinView.as_view()),
    path('product/<int:pk>/', views.ProductMixinView.as_view()),
    path('cartitem/', views.CartItemMixinView.as_view()),
    path('listcartitem/', views.CartItemListCreateAPIView.as_view())
]
