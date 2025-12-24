from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """
    Custom foydalanuvchi modeli.
    Telefon va email orqali login qilish imkoniyati bor.
    """
    first_name = None  # Django default first_name o'rniga ism ishlatamiz
    last_name = None   # Django default last_name o'rniga familiya

    ism = models.CharField(_("Ism"), max_length=255)
    familiya = models.CharField(_("Familiya"), max_length=255)
    rasm = models.ImageField(_("Rasm"), upload_to="users/", null=True, blank=True)
    telefon = models.CharField(_("Telefon raqam"), max_length=20, unique=True)
    email = models.EmailField(_("Email"), unique=True)

    yaratilgan_vaqt = models.DateTimeField(_("Yaratilgan vaqt"), auto_now_add=True)

    USERNAME_FIELD = "telefon"  # Login telefon orqali bo'ladi
    REQUIRED_FIELDS = ["email", "ism", "familiya"]

    def __str__(self):
        return f"{self.ism} {self.familiya}"

    class Meta:
        verbose_name = _("Foydalanuvchi")
        verbose_name_plural = _("Foydalanuvchilar")
