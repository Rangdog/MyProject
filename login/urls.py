from django.urls import path

from . import views

urlpatterns = [
    path('register/', views.RegisterAPIView.as_view()),
    path('login/', views.LoginAPIView.as_view()),
    path('user/', views.UserDetailView.as_view(), name='user-detail')
]
