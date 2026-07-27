from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProjeViewSet

# Router, bizim için otomatik olarak GET, POST, DELETE adreslerini oluşturur
router = DefaultRouter()
router.register(r'projeler', ProjeViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
from uygulamadi.views import register_user # (uygulamadi kısmını kendi app adınla değiştir)

urlpatterns = [
    # ... diğer url'lerin ...
    path('api/register/', register_user, name='register_user'),
]