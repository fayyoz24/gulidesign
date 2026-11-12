from rest_framework import viewsets, generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django_filters import rest_framework as f
from .models import *
from .serializers import *


class Public:
    """Ochiq endpoint: token umuman tekshirilmaydi (eski token ham xalaqit bermaydi)."""
    authentication_classes = []
    permission_classes = [permissions.AllowAny]


class ProductFilter(f.FilterSet):
    category = f.CharFilter(field_name="category__slug")
    min = f.NumberFilter(field_name="price", lookup_expr="gte")
    max = f.NumberFilter(field_name="price", lookup_expr="lte")
    class Meta:
        model = Product
        fields = ["category", "in_stock", "is_featured", "min", "max"]

class CategoryView(Public, viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all(); serializer_class = CategorySer; pagination_class = None

class ProductView(Public, viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.select_related("category").prefetch_related("images")
    serializer_class = ProductSer; filterset_class = ProductFilter
    ordering_fields = ["price", "created"]; search_fields = ["name_uz", "name_ru", "name_en"]

class PostView(Public, viewsets.ReadOnlyModelViewSet):
    queryset = Post.objects.filter(published=True); serializer_class = PostSer

class ContactView(Public, generics.CreateAPIView):
    serializer_class = ContactSer

class RegisterView(Public, generics.CreateAPIView):
    serializer_class = RegisterSer

class SettingsView(Public, APIView):
    def get(self, request):
        s, _ = SiteSettings.objects.get_or_create(pk=1)
        return Response(SettingsSer(s, context={"request": request}).data)

class OrderView(generics.ListCreateAPIView):
    """Faqat tizimga kirgan foydalanuvchi buyurtma bera oladi va o'z buyurtmalarini ko'radi."""
    serializer_class = OrderSer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self): return Order.objects.filter(user=self.request.user)