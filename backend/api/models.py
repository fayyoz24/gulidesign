from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name_uz = models.CharField(max_length=120); name_ru = models.CharField(max_length=120, blank=True); name_en = models.CharField(max_length=120, blank=True)
    slug = models.SlugField(unique=True)
    class Meta: verbose_name_plural = "Kategoriyalar"
    def __str__(self): return self.name_uz

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="products")
    name_uz = models.CharField(max_length=200); name_ru = models.CharField(max_length=200, blank=True); name_en = models.CharField(max_length=200, blank=True)
    description_uz = models.TextField(blank=True); description_ru = models.TextField(blank=True); description_en = models.TextField(blank=True)
    price = models.PositiveIntegerField(help_text="so'm (ming)"); old_price = models.PositiveIntegerField(null=True, blank=True)
    image = models.ImageField(upload_to="products/"); in_stock = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False); badge = models.CharField(max_length=30, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    class Meta: ordering = ["-created"]; verbose_name_plural = "Mahsulotlar"
    def __str__(self): return self.name_uz

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="products/")

class Order(models.Model):
    STATUS = [("new", "Yangi"), ("processing", "Jarayonda"), ("shipped", "Yuborildi"), ("done", "Yakunlandi"), ("cancelled", "Bekor")]
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=120); phone = models.CharField(max_length=30)
    address = models.TextField(); note = models.TextField(blank=True)
    total = models.PositiveIntegerField(default=0); status = models.CharField(max_length=12, choices=STATUS, default="new")
    created = models.DateTimeField(auto_now_add=True)
    class Meta: ordering = ["-created"]; verbose_name_plural = "Buyurtmalar"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    qty = models.PositiveIntegerField(default=1); price = models.PositiveIntegerField()

class Post(models.Model):
    title_uz = models.CharField(max_length=200); title_ru = models.CharField(max_length=200, blank=True); title_en = models.CharField(max_length=200, blank=True)
    body_uz = models.TextField(); body_ru = models.TextField(blank=True); body_en = models.TextField(blank=True)
    cover = models.ImageField(upload_to="blog/", blank=True); published = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    class Meta: ordering = ["-created"]; verbose_name_plural = "Blog"

class ContactMessage(models.Model):
    name = models.CharField(max_length=120); email = models.EmailField(); phone = models.CharField(max_length=30, blank=True)
    message = models.TextField(); is_read = models.BooleanField(default=False); created = models.DateTimeField(auto_now_add=True)
    class Meta: ordering = ["-created"]; verbose_name_plural = "Xabarlar"

class SiteSettings(models.Model):
    """Bitta yozuv: sayt kontaktlari, ijtimoiy tarmoqlar, bosh sahifa matnlari."""
    phone = models.CharField(max_length=30, default="+998 90 000 00 00"); email = models.EmailField(default="info@gulidesign.uz")
    address_uz = models.CharField(max_length=250, blank=True); address_ru = models.CharField(max_length=250, blank=True); address_en = models.CharField(max_length=250, blank=True)
    work_hours = models.CharField(max_length=120, default="Dushanba - Shanba: 9:00 - 18:00")
    instagram = models.URLField(blank=True); telegram = models.URLField(blank=True)
    hero_title_uz = models.CharField(max_length=120, default="Gul dizayn"); hero_title_ru = models.CharField(max_length=120, blank=True); hero_title_en = models.CharField(max_length=120, blank=True)
    hero_sub_uz = models.CharField(max_length=250, blank=True); hero_sub_ru = models.CharField(max_length=250, blank=True); hero_sub_en = models.CharField(max_length=250, blank=True)
    stat_products = models.PositiveIntegerField(default=500); stat_clients = models.PositiveIntegerField(default=1200); stat_masters = models.PositiveIntegerField(default=50)
    class Meta: verbose_name_plural = "Sayt sozlamalari"
