from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CategoryViewSet, SubCategoryViewSet, ShopViewSet,
    ProductViewSet, ProductReviewViewSet, ProductLikeViewSet,
    AdvertisementViewSet
)

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'subcategories', SubCategoryViewSet, basename='subcategory')
router.register(r'shops', ShopViewSet, basename='shop')
router.register(r'products', ProductViewSet, basename='product')
router.register(r'reviews', ProductReviewViewSet, basename='review')
router.register(r'likes', ProductLikeViewSet, basename='like')
router.register(r'advertisements', AdvertisementViewSet, basename='advertisement')

urlpatterns = [
    path('', include(router.urls)),
]
