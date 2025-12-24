# models.py
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _
from user.models import User


class Category(models.Model):
    nomi = models.CharField(_("Nomi"), max_length=255)
    tavsif = models.TextField(_("Tavsif"), blank=True)

    def __str__(self):
        return self.nomi

    class Meta:
        verbose_name = _("Kategoriya")
        verbose_name_plural = _("Kategoriyalar")


class SubCategory(models.Model):
    """Qism kategoriyalar (subkategoriyalar)"""
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="subcategories")
    nomi = models.CharField(_("Nomi"), max_length=255)
    tavsif = models.TextField(_("Tavsif"), blank=True)

    def __str__(self):
        return self.nomi

    class Meta:
        verbose_name = _("Qism kategoriya")
        verbose_name_plural = _("Qism kategoriyalar")


class Shop(models.Model):
    foydalanuvchi = models.ForeignKey(User, on_delete=models.CASCADE, related_name="shops")
    kompaniya_nomi = models.CharField(_("Kompaniya nomi"), max_length=255)
    brend_nomi = models.CharField(_("Brend nomi"), max_length=255)
    inn_stir = models.CharField(_("INN/STIR"), max_length=50, blank=True)
    yuridik_sertifikat = models.CharField(_("Yuridik sertifikat"), max_length=255, blank=True)
    direktor_ismi = models.CharField(_("Direktor ismi"), max_length=255)
    telefon_raqam_email = models.CharField(_("Telefon yoki email"), max_length=255)
    bizness_manzili = models.CharField(_("Biznes manzili"), max_length=255)
    brend_logotipi = models.ImageField(_("Brend logotipi"), upload_to="shops/", null=True, blank=True)
    jismoniy_tarmoqlar = models.TextField(_("Jismoniy tarmoqlar"), blank=True)
    pasport_seriyasi = models.CharField(_("Pasport seriyasi"), max_length=20, blank=True)
    tugilgan_kun = models.DateField(_("Tug'ilgan kun"), null=True, blank=True)
    yaratilgan_vaqt = models.DateTimeField(_("Yaratilgan vaqt"), auto_now_add=True)

    # Joylashuv uchun
    latitude = models.DecimalField(_("Kenglik"), max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(_("Uzunlik"), max_digits=9, decimal_places=6, null=True, blank=True)
    location = models.CharField(_("Manzil matni"), max_length=255, blank=True)
    muddati = models.DateField(_("Ro'yxatdan o'tish muddati"), null=True, blank=True)

    def __str__(self):
        return self.kompaniya_nomi

    class Meta:
        verbose_name = _("Do'kon")
        verbose_name_plural = _("Do'konlar")


class Product(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name="products")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="products")
    subcategory = models.ForeignKey(SubCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name="products")
    
    nomi = models.CharField(_("Nomi"), max_length=255)
    tavsif = models.TextField(_("Tavsif"))
    rasm = models.ImageField(_("Rasm"), upload_to="products/", null=True, blank=True)
    
    narx = models.DecimalField(
        _("Narx (so'm)"),
        max_digits=15,
        decimal_places=2,
        validators=[MinValueValidator(0)],
    )
    chegirma_narx = models.DecimalField(
        _("Chegirma narxi"),
        max_digits=15,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
    )
    chegirma_bormi = models.BooleanField(_("Chegirma mavjud"), default=False)
    
    yaratilgan_vaqt = models.DateTimeField(_("Yaratilgan vaqt"), auto_now_add=True)
    yangilangan_vaqt = models.DateTimeField(_("Yangilangan vaqt"), auto_now=True)

    def __str__(self):
        return self.nomi

    class Meta:
        verbose_name = _("Mahsulot")
        verbose_name_plural = _("Mahsulotlar")


class Advertisement(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="ads")
    tavsif = models.TextField(_("Tavsif"))
    rasm = models.ImageField(_("Rasm"), upload_to="ads/", null=True, blank=True)

    def __str__(self):
        return f"Reklama: {self.product.nomi}"

    class Meta:
        verbose_name = _("Reklama")
        verbose_name_plural = _("Reklamalar")


class ProductReview(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    tavsif = models.TextField(_("Sharh matni"))
    yulduz = models.IntegerField(
        _("Bahosi"),
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    yaratilgan_vaqt = models.DateTimeField(_("Yaratilgan vaqt"), auto_now_add=True)

    def __str__(self):
        return f"{self.user} — {self.product} ({self.yulduz} yulduz)"

    class Meta:
        verbose_name = _("Mahsulot sharhi")
        verbose_name_plural = _("Mahsulot sharhlari")


class ProductLike(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="likes")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likes")
    yaratilgan_vaqt = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["product", "user"], name="unique_product_like")
        ]
        verbose_name = _("Mahsulot like")
        verbose_name_plural = _("Mahsulot likelari")

    def __str__(self):
        return f"{self.user} yoqtirdi: {self.product}"

    nomi = models.CharField(_("Nomi"), max_length=255)
    tavsif = models.TextField(_("Tavsif"), blank=True)

    def __str__(self):
        return self.nomi

    class Meta:
        verbose_name = _("Kategoriya")
        verbose_name_plural = _("Kategoriyalar")


class SubCategory(models.Model):
    """Qism kategoriyalar (subkategoriyalar)"""
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="subcategories")
    nomi = models.CharField(_("Nomi"), max_length=255)
    tavsif = models.TextField(_("Tavsif"), blank=True)

    def __str__(self):
        return self.nomi

    class Meta:
        verbose_name = _("Qism kategoriya")
        verbose_name_plural = _("Qism kategoriyalar")


class Shop(models.Model):
    foydalanuvchi = models.ForeignKey(User, on_delete=models.CASCADE, related_name="shops")
    kompaniya_nomi = models.CharField(_("Kompaniya nomi"), max_length=255)
    brend_nomi = models.CharField(_("Brend nomi"), max_length=255)
    inn_stir = models.CharField(_("INN/STIR"), max_length=50, blank=True)
    yuridik_sertifikat = models.CharField(_("Yuridik sertifikat"), max_length=255, blank=True)
    direktor_ismi = models.CharField(_("Direktor ismi"), max_length=255)
    telefon_raqam_email = models.CharField(_("Telefon yoki email"), max_length=255)
    bizness_manzili = models.CharField(_("Biznes manzili"), max_length=255)
    brend_logotipi = models.ImageField(_("Brend logotipi"), upload_to="shops/", null=True, blank=True)
    jismoniy_tarmoqlar = models.TextField(_("Jismoniy tarmoqlar"), blank=True)
    pasport_seriyasi = models.CharField(_("Pasport seriyasi"), max_length=20, blank=True)
    tugilgan_kun = models.DateField(_("Tug'ilgan kun"), null=True, blank=True)
    yaratilgan_vaqt = models.DateTimeField(_("Yaratilgan vaqt"), auto_now_add=True)

    # Joylashuv uchun
    latitude = models.DecimalField(_("Kenglik"), max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(_("Uzunlik"), max_digits=9, decimal_places=6, null=True, blank=True)
    location = models.CharField(_("Manzil matni"), max_length=255, blank=True)
    muddati = models.DateField(_("Ro'yxatdan o'tish muddati"), null=True, blank=True)

    def __str__(self):
        return self.kompaniya_nomi

    class Meta:
        verbose_name = _("Do'kon")
        verbose_name_plural = _("Do'konlar")


class Product(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name="products")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="products")
    subcategory = models.ForeignKey(SubCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name="products")
    
    nomi = models.CharField(_("Nomi"), max_length=255)
    tavsif = models.TextField(_("Tavsif"))
    rasm = models.ImageField(_("Rasm"), upload_to="products/", null=True, blank=True)
    
    narx = models.DecimalField(
        _("Narx (so'm)"),
        max_digits=15,
        decimal_places=2,
        validators=[MinValueValidator(0)],
    )
    chegirma_narx = models.DecimalField(
        _("Chegirma narxi"),
        max_digits=15,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
    )
    chegirma_bormi = models.BooleanField(_("Chegirma mavjud"), default=False)
    
    yaratilgan_vaqt = models.DateTimeField(_("Yaratilgan vaqt"), auto_now_add=True)
    yangilangan_vaqt = models.DateTimeField(_("Yangilangan vaqt"), auto_now=True)

    def __str__(self):
        return self.nomi

    class Meta:
        verbose_name = _("Mahsulot")
        verbose_name_plural = _("Mahsulotlar")


class Advertisement(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="ads")
    tavsif = models.TextField(_("Tavsif"))
    rasm = models.ImageField(_("Rasm"), upload_to="ads/", null=True, blank=True)

    def __str__(self):
        return f"Reklama: {self.product.nomi}"

    class Meta:
        verbose_name = _("Reklama")
        verbose_name_plural = _("Reklamalar")


class ProductReview(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    tavsif = models.TextField(_("Sharh matni"))
    yulduz = models.IntegerField(
        _("Bahosi"),
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    yaratilgan_vaqt = models.DateTimeField(_("Yaratilgan vaqt"), auto_now_add=True)

    def __str__(self):
        return f"{self.user} — {self.product} ({self.yulduz} yulduz)"

    class Meta:
        verbose_name = _("Mahsulot sharhi")
        verbose_name_plural = _("Mahsulot sharhlari")


class ProductLike(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="likes")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likes")
    yaratilgan_vaqt = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["product", "user"], name="unique_product_like")
        ]
        verbose_name = _("Mahsulot like")
        verbose_name_plural = _("Mahsulot likelari")

    def __str__(self):
        return f"{self.user} yoqtirdi: {self.product}"