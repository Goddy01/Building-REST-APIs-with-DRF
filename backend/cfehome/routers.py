from rest_framework.routers import DefaultRouter
from products.viewsets import ProductViewset

router = DefaultRouter()
router.register('products', ProductViewset, basename='products')
urlpatterns = router.urls