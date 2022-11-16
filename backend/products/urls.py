from django.urls import path
from . import views

urlpatterns = [
    # for the class based API Views
    path('', views.ProductListCreateAPIView.as_view()),
    path('create/', views.ProductCreateAPIView.as_view()),
    path('list/', views.ProductListAPIView.as_view()),
    path('<int:pk>/', views.ProductDetailAPIView.as_view()),
    
    # for the func-based API View product_alt_view
    path('2/create/', views.product_alt_view),
    path('2/list/', views.product_alt_view),
    path('2/<int:pk>/', views.product_alt_view),
]