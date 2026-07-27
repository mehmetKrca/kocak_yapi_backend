from rest_framework import viewsets
from .models import Proje
from .serializers import ProjeSerializer

class ProjeViewSet(viewsets.ModelViewSet):
    # Projeleri en son oluşturulana göre (yeniden eskiye) sıralayarak çekeceğiz
    queryset = Proje.objects.all().order_by('-olusturma_tarihi')
    serializer_class = ProjeSerializer