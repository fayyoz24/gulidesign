from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views
r = DefaultRouter()
r.register("categories", views.CategoryView); r.register("products", views.ProductView); r.register("posts", views.PostView)
urlpatterns = r.urls + [
    path("contact/", views.ContactView.as_view()), path("orders/", views.OrderView.as_view()),
    path("settings/", views.SettingsView.as_view()), path("auth/register/", views.RegisterView.as_view()),
    path("auth/login/", TokenObtainPairView.as_view()), path("auth/refresh/", TokenRefreshView.as_view()),
]
