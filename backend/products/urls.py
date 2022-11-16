from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.ProductCreateAPIView.as_view()),
    path('<int:pk>/', views.ProductDetailAPIView.as_view())
]