# Chegirma Platform API

Django REST Framework bilan yaratilgan to'liq Swagger dokumentatsiyali API.

## O'rnatish

```bash
# Virtual environment yaratish
python -m venv venv
source venv/bin/activate  # Linux/Mac
# yoki
venv\Scripts\activate  # Windows

# Paketlarni o'rnatish
pip install -r requirements.txt

# Migratsiyalarni qo'llash
python manage.py migrate

# Superuser yaratish
python manage.py createsuperuser

# Serverni ishga tushirish
python manage.py runserver
```

## API Endpoints

Server ishga tushgandan so'ng quyidagi URL'larga kiring:

- **Swagger UI**: http://127.0.0.1:8000/swagger/
- **ReDoc**: http://127.0.0.1:8000/redoc/
- **Admin Panel**: http://127.0.0.1:8000/admin/

## API Struktura

### User API (`/api/v1/auth/`)
- `GET /api/v1/auth/users/` - Barcha foydalanuvchilar
- `POST /api/v1/auth/users/` - Yangi foydalanuvchi yaratish
- `GET /api/v1/auth/users/{id}/` - Foydalanuvchi ma'lumoti
- `GET /api/v1/auth/users/me/` - Joriy foydalanuvchi
- `GET /api/v1/auth/users/{id}/shops/` - Foydalanuvchining do'konlari

### Kategoriya API (`/api/v1/`)
- `GET /api/v1/categories/` - Barcha kategoriyalar
- `POST /api/v1/categories/` - Yangi kategoriya
- `GET /api/v1/categories/{id}/subcategories/` - Kategoriya subkategoriyalari
- `GET /api/v1/categories/{id}/products/` - Kategoriya mahsulotlari

### SubKategoriya API
- `GET /api/v1/subcategories/` - Barcha subkategoriyalar
- `POST /api/v1/subcategories/` - Yangi subkategoriya

### Do'kon API
- `GET /api/v1/shops/` - Barcha do'konlar
- `POST /api/v1/shops/` - Yangi do'kon yaratish
- `GET /api/v1/shops/{id}/` - Do'kon ma'lumoti
- `GET /api/v1/shops/{id}/products/` - Do'kon mahsulotlari

### Mahsulot API
- `GET /api/v1/products/` - Barcha mahsulotlar
- `POST /api/v1/products/` - Yangi mahsulot
- `GET /api/v1/products/{id}/` - Mahsulot detallari
- `GET /api/v1/products/discounted/` - Chegirmadagi mahsulotlar
- `POST /api/v1/products/{id}/like/` - Mahsulotni like qilish
- `DELETE /api/v1/products/{id}/unlike/` - Like'ni olib tashlash
- `GET /api/v1/products/{id}/reviews/` - Mahsulot sharhlari

### Sharh va Like API
- `GET /api/v1/reviews/` - Barcha sharhlar
- `POST /api/v1/reviews/` - Yangi sharh qo'shish
- `GET /api/v1/likes/` - Barcha like'lar

### Reklama API
- `GET /api/v1/advertisements/` - Barcha reklamalar
- `POST /api/v1/advertisements/` - Yangi reklama

## Xususiyatlar

✅ **To'liq CRUD operatsiyalari** - Barcha modellar uchun
✅ **Swagger/OpenAPI dokumentatsiya** - Interaktiv API docs
✅ **Filtrlash va qidiruv** - Barcha endpoint'larda
✅ **Pagination** - 10 ta element sahifada
✅ **Authentication** - Session va Basic Auth
✅ **Permission system** - Autentifikatsiya talab qilinadigan endpoint'lar
✅ **Media file upload** - Rasm yuklash imkoniyati
✅ **Custom User Model** - Telefon orqali login
✅ **Related data** - Nested serializers
✅ **Admin panel** - Django admin optimizatsiya qilingan

## Filtrlash va qidiruv

Misol:
```
GET /api/v1/products/?search=telefon
GET /api/v1/products/?category=1
GET /api/v1/products/?chegirma_bormi=true
GET /api/v1/products/?ordering=-yaratilgan_vaqt
GET /api/v1/shops/{id}/products/?has_discount=true
```

## Teknologiyalar

- Django 5.2.9
- Django REST Framework 3.16.1
- drf-yasg 1.21.11 (Swagger)
- django-filter 25.2
- Pillow 12.0.0

## Loyiha strukturasi

```
Chegirma/
├── core/           # Asosiy settings va URL config
├── user/           # User app (foydalanuvchi)
├── categoriya/     # Kategoriya, Shop, Product modellari
├── media/          # Media fayllar
├── manage.py
└── requirements.txt
```
