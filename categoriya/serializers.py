from rest_framework import serializers
from .models import Category, SubCategory, Shop, Product, Advertisement, ProductReview, ProductLike


class CategorySerializer(serializers.ModelSerializer):
    """Kategoriya serializer"""
    subcategories_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = ['id', 'nomi', 'tavsif', 'subcategories_count']
        
    def get_subcategories_count(self, obj):
        return obj.subcategories.count()


class SubCategorySerializer(serializers.ModelSerializer):
    """SubKategoriya serializer"""
    category_name = serializers.CharField(source='category.nomi', read_only=True)
    
    class Meta:
        model = SubCategory
        fields = ['id', 'category', 'category_name', 'nomi', 'tavsif']


class ShopSerializer(serializers.ModelSerializer):
    """Do'kon serializer"""
    foydalanuvchi_info = serializers.SerializerMethodField()
    products_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Shop
        fields = [
            'id', 'foydalanuvchi', 'foydalanuvchi_info', 'kompaniya_nomi', 
            'brend_nomi', 'inn_stir', 'yuridik_sertifikat', 'direktor_ismi',
            'telefon_raqam_email', 'bizness_manzili', 'brend_logotipi',
            'jismoniy_tarmoqlar', 'pasport_seriyasi', 'tugilgan_kun',
            'latitude', 'longitude', 'location', 'muddati',
            'yaratilgan_vaqt', 'products_count'
        ]
        read_only_fields = ['yaratilgan_vaqt']
        
    def get_foydalanuvchi_info(self, obj):
        return {
            'id': obj.foydalanuvchi.id,
            'ism': obj.foydalanuvchi.ism,
            'familiya': obj.foydalanuvchi.familiya,
            'telefon': obj.foydalanuvchi.telefon
        }
        
    def get_products_count(self, obj):
        return obj.products.count()


class ProductLikeSerializer(serializers.ModelSerializer):
    """Mahsulot like serializer"""
    user_info = serializers.SerializerMethodField()
    
    class Meta:
        model = ProductLike
        fields = ['id', 'product', 'user', 'user_info', 'yaratilgan_vaqt']
        read_only_fields = ['yaratilgan_vaqt']
        
    def get_user_info(self, obj):
        return {
            'id': obj.user.id,
            'ism': obj.user.ism,
            'familiya': obj.user.familiya
        }


class ProductReviewSerializer(serializers.ModelSerializer):
    """Mahsulot sharh serializer"""
    user_info = serializers.SerializerMethodField()
    
    class Meta:
        model = ProductReview
        fields = ['id', 'product', 'user', 'user_info', 'tavsif', 'yulduz', 'yaratilgan_vaqt']
        read_only_fields = ['yaratilgan_vaqt']
        
    def get_user_info(self, obj):
        return {
            'id': obj.user.id,
            'ism': obj.user.ism,
            'familiya': obj.user.familiya,
            'rasm': obj.user.rasm.url if obj.user.rasm else None
        }


class ProductSerializer(serializers.ModelSerializer):
    """Mahsulot serializer"""
    shop_name = serializers.CharField(source='shop.kompaniya_nomi', read_only=True)
    category_name = serializers.CharField(source='category.nomi', read_only=True)
    subcategory_name = serializers.CharField(source='subcategory.nomi', read_only=True)
    reviews_count = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = [
            'id', 'shop', 'shop_name', 'category', 'category_name',
            'subcategory', 'subcategory_name', 'nomi', 'tavsif', 'rasm',
            'narx', 'chegirma_narx', 'chegirma_bormi',
            'yaratilgan_vaqt', 'yangilangan_vaqt',
            'reviews_count', 'likes_count', 'average_rating'
        ]
        read_only_fields = ['yaratilgan_vaqt', 'yangilangan_vaqt']
        
    def get_reviews_count(self, obj):
        return obj.reviews.count()
        
    def get_likes_count(self, obj):
        return obj.likes.count()
        
    def get_average_rating(self, obj):
        reviews = obj.reviews.all()
        if reviews.exists():
            from django.db.models import Avg
            return reviews.aggregate(Avg('yulduz'))['yulduz__avg']
        return None


class ProductDetailSerializer(ProductSerializer):
    """Mahsulot detali serializer"""
    reviews = ProductReviewSerializer(many=True, read_only=True)
    likes = ProductLikeSerializer(many=True, read_only=True)
    
    class Meta(ProductSerializer.Meta):
        fields = ProductSerializer.Meta.fields + ['reviews', 'likes']


class AdvertisementSerializer(serializers.ModelSerializer):
    """Reklama serializer"""
    product_name = serializers.CharField(source='product.nomi', read_only=True)
    
    class Meta:
        model = Advertisement
        fields = ['id', 'product', 'product_name', 'tavsif', 'rasm']
