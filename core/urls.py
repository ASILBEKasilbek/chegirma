"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Swagger/OpenAPI sozlamalari
schema_view = get_schema_view(
    openapi.Info(
        title="Chegirma API",
        default_version='v1',
        description="""
        # Chegirma platformasi API dokumentatsiyasi
        
        Bu API Chegirma platformasi uchun to'liq REST API hisoblanadi.
        
        ## Asosiy xususiyatlar:
        - **Foydalanuvchilar**: Ro'yxatdan o'tish va profil boshqaruvi
        - **Kategoriyalar**: Mahsulot kategoriyalari va subkategoriyalari
        - **Do'konlar**: Do'konlarni ro'yxatga olish va boshqarish
        - **Mahsulotlar**: Mahsulotlarni qo'shish, tahrirlash va ko'rish
        - **Sharhlar va Likelar**: Mahsulotlarga sharh va baho qo'yish
        - **Reklamalar**: Mahsulot reklamalari
        
        ## Autentifikatsiya:
        - Session Authentication
        - Basic Authentication
        
        ## Filtrlash va qidiruv:
        Barcha endpoint'larda filtrlash, qidiruv va tartibga solish imkoniyatlari mavjud.
        """,
        terms_of_service="https://www.chegirma.uz/terms/",
        contact=openapi.Contact(email="support@chegirma.uz"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # API endpoints
    path('api/v1/auth/', include('user.urls')),
    path('api/v1/', include('categoriya.urls')),
    
    # Swagger UI endpoints
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui-root'),
    
    # DRF browsable API login
    path('api-auth/', include('rest_framework.urls')),
]

# Media files uchun URL
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

