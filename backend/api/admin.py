from django.contrib import admin
from .models import *

class ImgInline(admin.TabularInline): model = ProductImage; extra = 1
class ItemInline(admin.TabularInline): model = OrderItem; extra = 0; readonly_fields = ["product", "qty", "price"]
@admin.register(Category)
class CatA(admin.ModelAdmin): list_display = ["name_uz", "slug"]; prepopulated_fields = {"slug": ("name_uz",)}
@admin.register(Product)
class ProdA(admin.ModelAdmin):
    list_display = ["name_uz", "category", "price", "in_stock", "is_featured"]; list_editable = ["price", "in_stock", "is_featured"]
    list_filter = ["category", "in_stock", "is_featured"]; search_fields = ["name_uz"]; inlines = [ImgInline]
@admin.register(Order)
class OrdA(admin.ModelAdmin):
    list_display = ["id", "name", "phone", "total", "status", "created"]; list_editable = ["status"]; list_filter = ["status"]; inlines = [ItemInline]
@admin.register(Post)
class PostA(admin.ModelAdmin): list_display = ["title_uz", "published", "created"]; list_editable = ["published"]
@admin.register(ContactMessage)
class MsgA(admin.ModelAdmin): list_display = ["name", "email", "phone", "is_read", "created"]; list_editable = ["is_read"]
@admin.register(SiteSettings)
class SetA(admin.ModelAdmin):
    def has_add_permission(self, r): return not SiteSettings.objects.exists()
    def has_delete_permission(self, r, o=None): return False
