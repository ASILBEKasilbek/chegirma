from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import User
from .serializers import UserSerializer, UserCreateSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    User CRUD operations
    
    list: Barcha foydalanuvchilarni ko'rish
    create: Yangi foydalanuvchi yaratish
    retrieve: Bitta foydalanuvchi ma'lumotini ko'rish
    update: Foydalanuvchi ma'lumotini yangilash
    partial_update: Foydalanuvchi ma'lumotini qisman yangilash
    destroy: Foydalanuvchini o'chirish
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['ism', 'familiya', 'telefon', 'email']
    ordering_fields = ['yaratilgan_vaqt', 'ism']
    ordering = ['-yaratilgan_vaqt']
    
    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        return UserSerializer
    
    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        return [IsAuthenticated()]
    
    @swagger_auto_schema(
        method='get',
        operation_description="Joriy foydalanuvchi ma'lumotlarini olish",
        responses={200: UserSerializer()}
    )
    @action(detail=False, methods=['get'])
    def me(self, request):
        """Joriy foydalanuvchi ma'lumotlarini qaytaradi"""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
    
    @swagger_auto_schema(
        method='get',
        operation_description="Foydalanuvchining do'konlarini ko'rish"
    )
    @action(detail=True, methods=['get'])
    def shops(self, request, pk=None):
        """Foydalanuvchining barcha do'konlarini qaytaradi"""
        user = self.get_object()
        from categoriya.serializers import ShopSerializer
        shops = user.shops.all()
        serializer = ShopSerializer(shops, many=True)
        return Response(serializer.data)
