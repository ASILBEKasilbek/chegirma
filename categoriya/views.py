from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import (
    Category, SubCategory, Shop, Product, 
    Advertisement, ProductReview, ProductLike
)
from .serializers import (
    CategorySerializer, SubCategorySerializer, ShopSerializer,
    ProductSerializer, ProductDetailSerializer, AdvertisementSerializer,
    ProductReviewSerializer, ProductLikeSerializer
)


class CategoryViewSet(viewsets.ModelViewSet):
    """
    Kategoriya CRUD operations
    
    list: Barcha kategoriyalarni ko'rish
    create: Yangi kategoriya yaratish
    retrieve: Bitta kategoriya ma'lumotini ko'rish
    update: Kategoriya ma'lumotini yangilash
    destroy: Kategoriyani o'chirish
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nomi', 'tavsif']
    ordering_fields = ['nomi']
    ordering = ['nomi']
    
    @swagger_auto_schema(
        method='get',
        operation_description="Kategoriyaning barcha subkategoriyalarini ko'rish"
    )
    @action(detail=True, methods=['get'])
    def subcategories(self, request, pk=None):
        """Kategoriyaning barcha subkategoriyalarini qaytaradi"""
        category = self.get_object()
        subcategories = category.subcategories.all()
        serializer = SubCategorySerializer(subcategories, many=True)
        return Response(serializer.data)
    
    @swagger_auto_schema(
        method='get',
        operation_description="Kategoriyaga tegishli mahsulotlarni ko'rish"
    )
    @action(detail=True, methods=['get'])
    def products(self, request, pk=None):
        """Kategoriyaga tegishli barcha mahsulotlarni qaytaradi"""
        category = self.get_object()
        products = category.products.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


class SubCategoryViewSet(viewsets.ModelViewSet):
    """
    SubKategoriya CRUD operations
    """
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['category']
    search_fields = ['nomi', 'tavsif']
    
    @swagger_auto_schema(
        method='get',
        operation_description="Subkategoriyaga tegishli mahsulotlarni ko'rish"
    )
    @action(detail=True, methods=['get'])
    def products(self, request, pk=None):
        """Subkategoriyaga tegishli barcha mahsulotlarni qaytaradi"""
        subcategory = self.get_object()
        products = subcategory.products.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


class ShopViewSet(viewsets.ModelViewSet):
    """
    Do'kon CRUD operations
    
    list: Barcha do'konlarni ko'rish
    create: Yangi do'kon yaratish
    retrieve: Bitta do'kon ma'lumotini ko'rish
    update: Do'kon ma'lumotini yangilash
    destroy: Do'konni o'chirish
    """
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['foydalanuvchi']
    search_fields = ['kompaniya_nomi', 'brend_nomi', 'bizness_manzili']
    ordering_fields = ['yaratilgan_vaqt', 'kompaniya_nomi']
    ordering = ['-yaratilgan_vaqt']
    
    @swagger_auto_schema(
        method='get',
        operation_description="Do'konning barcha mahsulotlarini ko'rish"
    )
    @action(detail=True, methods=['get'])
    def products(self, request, pk=None):
        """Do'konning barcha mahsulotlarini qaytaradi"""
        shop = self.get_object()
        products = shop.products.all()
        
        # Chegirma filtri
        has_discount = request.query_params.get('has_discount', None)
        if has_discount is not None:
            products = products.filter(chegirma_bormi=has_discount.lower() == 'true')
        
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


class ProductViewSet(viewsets.ModelViewSet):
    """
    Mahsulot CRUD operations
    
    list: Barcha mahsulotlarni ko'rish
    create: Yangi mahsulot yaratish
    retrieve: Bitta mahsulot ma'lumotini ko'rish
    update: Mahsulot ma'lumotini yangilash
    destroy: Mahsulotni o'chirish
    """
    queryset = Product.objects.select_related('shop', 'category', 'subcategory').all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['shop', 'category', 'subcategory', 'chegirma_bormi']
    search_fields = ['nomi', 'tavsif']
    ordering_fields = ['yaratilgan_vaqt', 'narx', 'nomi']
    ordering = ['-yaratilgan_vaqt']
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ProductDetailSerializer
        return ProductSerializer
    
    @swagger_auto_schema(
        method='get',
        operation_description="Chegirmadagi mahsulotlarni ko'rish"
    )
    @action(detail=False, methods=['get'])
    def discounted(self, request):
        """Chegirmadagi mahsulotlarni qaytaradi"""
        products = self.queryset.filter(chegirma_bormi=True)
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)
    
    @swagger_auto_schema(
        method='post',
        operation_description="Mahsulotni like qilish",
        responses={
            201: openapi.Response('Like qo\'shildi'),
            400: openapi.Response('Xato')
        }
    )
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def like(self, request, pk=None):
        """Mahsulotni like qilish"""
        product = self.get_object()
        like, created = ProductLike.objects.get_or_create(
            product=product,
            user=request.user
        )
        if created:
            return Response({'status': 'like qo\'shildi'}, status=status.HTTP_201_CREATED)
        return Response({'status': 'allaqachon like qilgansiz'}, status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(
        method='delete',
        operation_description="Mahsulotdan like ni olib tashlash"
    )
    @action(detail=True, methods=['delete'], permission_classes=[IsAuthenticated])
    def unlike(self, request, pk=None):
        """Mahsulotdan like ni olib tashlash"""
        product = self.get_object()
        try:
            like = ProductLike.objects.get(product=product, user=request.user)
            like.delete()
            return Response({'status': 'like olib tashlandi'}, status=status.HTTP_204_NO_CONTENT)
        except ProductLike.DoesNotExist:
            return Response({'status': 'like topilmadi'}, status=status.HTTP_404_NOT_FOUND)
    
    @swagger_auto_schema(
        method='get',
        operation_description="Mahsulotning barcha sharhlarini ko'rish"
    )
    @action(detail=True, methods=['get'])
    def reviews(self, request, pk=None):
        """Mahsulotning barcha sharhlarini qaytaradi"""
        product = self.get_object()
        reviews = product.reviews.all().order_by('-yaratilgan_vaqt')
        serializer = ProductReviewSerializer(reviews, many=True)
        return Response(serializer.data)


class ProductReviewViewSet(viewsets.ModelViewSet):
    """
    Mahsulot sharhlari CRUD operations
    """
    queryset = ProductReview.objects.select_related('product', 'user').all()
    serializer_class = ProductReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['product', 'user', 'yulduz']
    ordering_fields = ['yaratilgan_vaqt', 'yulduz']
    ordering = ['-yaratilgan_vaqt']
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ProductLikeViewSet(viewsets.ModelViewSet):
    """
    Mahsulot likelari CRUD operations
    """
    queryset = ProductLike.objects.select_related('product', 'user').all()
    serializer_class = ProductLikeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['product', 'user']
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class AdvertisementViewSet(viewsets.ModelViewSet):
    """
    Reklama CRUD operations
    """
    queryset = Advertisement.objects.select_related('product').all()
    serializer_class = AdvertisementSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['product']
    search_fields = ['tavsif']

