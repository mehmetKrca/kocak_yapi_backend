from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import HesapProfili, Proje, FiyatTablosu
from .serializers import HesapProfiliSerializer, ProjeSerializer, FiyatTablosuSerializer

class HesapProfiliViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = HesapProfiliSerializer

    def get_queryset(self):
        return HesapProfili.objects.filter(user=self.request.user, aktif_mi=True)

class ProjeViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ProjeSerializer

    def get_queryset(self):
        aktif_hesap, _ = HesapProfili.objects.get_or_create(
            user=self.request.user,
            defaults={'firma_adi': self.request.user.username or "Firma / Usta"}
        )
        return Proje.objects.filter(hesap=aktif_hesap).order_by('-id')

    def perform_create(self, serializer):
        aktif_hesap, _ = HesapProfili.objects.get_or_create(
            user=self.request.user,
            defaults={'firma_adi': self.request.user.username or "Firma / Usta"}
        )
        serializer.save(hesap=aktif_hesap)

class FiyatTablosuViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = FiyatTablosuSerializer

    def get_queryset(self):
        aktif_hesap, _ = HesapProfili.objects.get_or_create(
            user=self.request.user,
            defaults={'firma_adi': self.request.user.username or "Firma / Usta"}
        )
        return FiyatTablosu.objects.filter(hesap=aktif_hesap)

    def perform_create(self, serializer):
        aktif_hesap, _ = HesapProfili.objects.get_or_create(
            user=self.request.user,
            defaults={'firma_adi': self.request.user.username or "Firma / Usta"}
        )
        serializer.save(hesap=aktif_hesap)
        from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User

@api_view(['POST'])
@permission_classes([AllowAny])  # Giriş yapmamış herkes kayıt olabilsin diye
def register_user(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not username or not password:
        return Response({"error": "Kullanıcı adı ve şifre zorunludur."}, status=status.HTTP_400_BAD_REQUEST)
        
    if User.objects.filter(username=username).exists():
        return Response({"error": "Bu kullanıcı adı zaten alınmış."}, status=status.HTTP_400_BAD_REQUEST)
        
    user = User.objects.create_user(username=username, password=password)
    return Response({"message": "Kayıt başarıyla oluşturuldu! 14 gün ücretsiz denemeniz başladı."}, status=status.HTTP_201_CREATED)