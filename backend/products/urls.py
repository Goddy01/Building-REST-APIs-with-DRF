from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProductListCreateAPIView.as_view()),
    path('create/', views.ProductCreateAPIView.as_view()),
    path('list/', views.ProductListAPIView.as_view()),
    path('<int:pk>/', views.ProductDetailAPIView.as_view())
]