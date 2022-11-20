from rest_framework.routers import DefaultRouter
from products.viewsets import ProductViewset, ProductGenericViewSet

router = DefaultRouter()
router.register('products', ProductViewset, basename='products')
urlpatterns = router.urls