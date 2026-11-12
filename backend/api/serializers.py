from django.contrib.auth.models import User
from rest_framework import serializers
from .models import *

class TR(serializers.ModelSerializer):
    tr = []
    def to_representation(self, o):
        d = super().to_representation(o); lang = self.context["request"].GET.get("lang", "uz")
        for f in self.tr:
            uz = d.pop(f + "_uz", ""); ru = d.pop(f + "_ru", ""); en = d.pop(f + "_en", "")
            d[f] = {"uz": uz, "ru": ru, "en": en}.get(lang) or uz
        return d

class CategorySer(TR):
    tr = ["name"]
    class Meta: model = Category; fields = "__all__"
class ProductSer(TR):
    tr = ["name", "description"]
    category_slug = serializers.CharField(source="category.slug", read_only=True)
    images = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = "__all__"

    def get_images(self, obj):
        request = self.context["request"]
        return [request.build_absolute_uri(i.image.url) for i in obj.images.all()]
class PostSer(TR):
    tr = ["title", "body"]
    class Meta: model = Post; fields = "__all__"
class SettingsSer(TR):
    tr = ["address", "hero_title", "hero_sub"]
    class Meta: model = SiteSettings; fields = "__all__"
class ContactSer(serializers.ModelSerializer):
    class Meta: model = ContactMessage; fields = ["name", "email", "phone", "message"]
class ItemSer(serializers.Serializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.filter(in_stock=True)); qty = serializers.IntegerField(min_value=1)
class OrderSer(serializers.ModelSerializer):
    items = ItemSer(many=True, write_only=True)
    class Meta: model = Order; fields = ["id", "name", "phone", "address", "note", "items", "total", "status", "created"]; read_only_fields = ["total", "status", "created"]
    def create(self, v):
        items = v.pop("items"); user = self.context["request"].user
        o = Order.objects.create(user=self.context["request"].user, **v); t = 0
        for i in items:
            OrderItem.objects.create(order=o, product=i["product"], qty=i["qty"], price=i["product"].price); t += i["product"].price * i["qty"]
        o.total = t; o.save(); return o
class RegisterSer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=False, allow_blank=True, max_length=60)
    email = serializers.EmailField(error_messages={
        "required": "Emailni kiriting.", "blank": "Emailni kiriting.",
        "invalid": "Email noto'g'ri yozilgan. Masalan: ali@mail.uz"})
    password = serializers.CharField(write_only=True, min_length=6, error_messages={
        "required": "Parolni kiriting.", "blank": "Parolni kiriting.",
        "min_length": "Parol kamida 6 ta belgidan iborat bo'lishi kerak."})

    class Meta:
        model = User
        fields = ["first_name", "email", "password"]

    def validate_email(self, v):
        v = v.lower().strip()
        if User.objects.filter(username=v).exists():
            raise serializers.ValidationError("Bu email bilan ro'yxatdan o'tilgan. Kirish sahifasiga o'ting.")
        return v

    def create(self, v):
        return User.objects.create_user(username=v["email"], email=v["email"],
                                        password=v["password"], first_name=v.get("first_name", ""))