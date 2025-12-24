from django.contrib import admin
from .models import (
    Category, SubCategory, Shop, Product,
    Advertisement, ProductReview, ProductLike
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['nomi', 'tavsif']
    search_fields = ['nomi']


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ['nomi', 'category', 'tavsif']
    list_filter = ['category']
    search_fields = ['nomi']


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ['kompaniya_nomi', 'brend_nomi', 'foydalanuvchi', 'yaratilgan_vaqt']
    list_filter = ['yaratilgan_vaqt']
    search_fields = ['kompaniya_nomi', 'brend_nomi', 'inn_stir']
    date_hierarchy = 'yaratilgan_vaqt'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['nomi', 'shop', 'category', 'narx', 'chegirma_bormi', 'yaratilgan_vaqt']
    list_filter = ['chegirma_bormi', 'category', 'yaratilgan_vaqt']
    search_fields = ['nomi', 'tavsif']
    date_hierarchy = 'yaratilgan_vaqt'


@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ['product', 'tavsif']
    search_fields = ['tavsif']


@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'yulduz', 'yaratilgan_vaqt']
    list_filter = ['yulduz', 'yaratilgan_vaqt']
    search_fields = ['tavsif', 'product__nomi', 'user__ism']
    date_hierarchy = 'yaratilgan_vaqt'


@admin.register(ProductLike)
class ProductLikeAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'yaratilgan_vaqt']
    list_filter = ['yaratilgan_vaqt']
    search_fields = ['product__nomi', 'user__ism']

