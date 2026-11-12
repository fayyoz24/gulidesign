import os
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.getenv("SECRET_KEY", "change-me")
DEBUG = os.getenv("DEBUG", "1") == "1"
ALLOWED_HOSTS = ["gulidesign.uz", "www.gulidesign.uz", "localhost", "127.0.0.1", "gulidesign.pythonanywhere.com"]
CSRF_TRUSTED_ORIGINS = ["https://gulidesign.uz", "https://www.gulidesign.uz", "https://gulidesign.pythonanywhere.com", "http://localhost:5172", "https://gulidesign-vclk.vercel.app"]
CORS_ALLOWED_ORIGINS = ["https://gulidesign.uz", "https://www.gulidesign.uz", "http://localhost:5172", "https://gulidesign.pythonanywhere.com", "https://gulidesign-vclk.vercel.app"]
INSTALLED_APPS = ["django.contrib.admin", "django.contrib.auth", "django.contrib.contenttypes",
    "django.contrib.sessions", "django.contrib.messages", "django.contrib.staticfiles",
    "rest_framework", "corsheaders", "django_filters", "api"]
MIDDLEWARE = ["corsheaders.middleware.CorsMiddleware", "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware", "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware", "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware"]
ROOT_URLCONF = "config.urls"
TEMPLATES = [{"BACKEND": "django.template.backends.django.DjangoTemplates", "DIRS": [], "APP_DIRS": True,
    "OPTIONS": {"context_processors": ["django.template.context_processors.request",
    "django.contrib.auth.context_processors.auth", "django.contrib.messages.context_processors.messages"]}}]
DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": BASE_DIR / "db.sqlite3"}}  # prod: PostgreSQL
STATIC_URL = "/static/"; STATIC_ROOT = BASE_DIR / "static"
MEDIA_URL = "/media/"; MEDIA_ROOT = BASE_DIR / "media"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
LANGUAGE_CODE = "uz"; TIME_ZONE = "Asia/Tashkent"; USE_TZ = True
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": ["rest_framework_simplejwt.authentication.JWTAuthentication"],
    "DEFAULT_FILTER_BACKENDS": ["django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.OrderingFilter", "rest_framework.filters.SearchFilter"],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination", "PAGE_SIZE": 24,
}
