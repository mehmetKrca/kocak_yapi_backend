from django.db import models
from django.contrib.auth.models import User

# 1. ABONELİK PAKETLERİ (Sadece senin yönettiğin tablo)
class AbonelikPaketi(models.Model):
    paket_adi = models.CharField(max_length=100, verbose_name="Paket Adı (Örn: Bireysel, İşletme)")
    aylik_fiyat = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Aylık Ücret (TL)")
    ozellikler = models.TextField(verbose_name="Paket Özellikleri", blank=True, null=True)

    class Meta:
        verbose_name = "Abonelik Paketi"
        verbose_name_plural = "1 - Abonelik Paketleri"

    def __str__(self):
        return f"{self.paket_adi} - {self.aylik_fiyat} TL"


# 2. HESAP PROFİLİ (Kayıt olan ustalar/işletmeler)
class HesapProfili(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profil', verbose_name="Kullanıcı Giriş Bilgisi")
    paket = models.ForeignKey(AbonelikPaketi, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Seçilen Abonelik Paketi")
    
    firma_adi = models.CharField(max_length=255, verbose_name="Firma veya Usta Adı")
    telefon = models.CharField(max_length=20, blank=True, null=True, verbose_name="Telefon Numarası")
    varsayilan_seri = models.IntegerField(default=70, verbose_name="Varsayılan PVC Serisi") 
    aktif_mi = models.BooleanField(default=True, verbose_name="Aktif Müşteri mi?")

    class Meta:
        verbose_name = "Hesap Profili"
        verbose_name_plural = "2 - Hesap Profilleri"

    def __str__(self):
        return self.firma_adi


# 3. FİYAT TABLOSU (Ustaların kendi gireceği fiyatlar)
class FiyatTablosu(models.Model):
    hesap = models.ForeignKey(HesapProfili, on_delete=models.CASCADE, related_name='fiyatlar', verbose_name="Ait Olduğu Hesap")
    
    RENK_SECENEKLERI = [
        ('beyaz', 'Beyaz'),
        ('antrasit', 'Antrasit'),
        ('altin_mese', 'Altın Meşe')
    ]
    renk = models.CharField(max_length=20, choices=RENK_SECENEKLERI, default='beyaz', verbose_name="Profil Rengi")
    
    # --- FİYAT ALANLARI ---
    kasa = models.DecimalField(max_digits=10, decimal_places=2, default=150, verbose_name="UPVC Kasa (mt)")
    ortakayit = models.DecimalField(max_digits=10, decimal_places=2, default=150, verbose_name="UPVC Orta Kayıt (mt)")
    pencereKanadi = models.DecimalField(max_digits=10, decimal_places=2, default=150, verbose_name="UPVC Pencere Kanadı (mt)")
    kapiKanadi = models.DecimalField(max_digits=10, decimal_places=2, default=150, verbose_name="UPVC Kapı Kanadı (mt)")
    surmeKasa = models.DecimalField(max_digits=10, decimal_places=2, default=150, verbose_name="UPVC Sürme Kasa (mt)")
    surmeKanadi = models.DecimalField(max_digits=10, decimal_places=2, default=150, verbose_name="UPVC Sürme Kanat (mt)")
    
    aluKasa = models.DecimalField(max_digits=10, decimal_places=2, default=400, verbose_name="Alüminyum Kasa (mt)")
    aluOrtakayit = models.DecimalField(max_digits=10, decimal_places=2, default=400, verbose_name="Alüminyum Orta Kayıt (mt)")
    
    cam = models.DecimalField(max_digits=10, decimal_places=2, default=800, verbose_name="Cam (m2)")
    
    tekAcilim = models.DecimalField(max_digits=10, decimal_places=2, default=350, verbose_name="Tek Açılım (Adet)")
    ciftAcilim = models.DecimalField(max_digits=10, decimal_places=2, default=600, verbose_name="Çift Açılım (Adet)")
    
    plisePerdeM2 = models.DecimalField(max_digits=10, decimal_places=2, default=600, verbose_name="Plise Perde (m2)")
    surguluSineklikM2 = models.DecimalField(max_digits=10, decimal_places=2, default=750, verbose_name="Sürgülü Sineklik (m2)")

    class Meta:
        unique_together = ('hesap', 'renk') 
        verbose_name = "Fiyat Tablosu"
        verbose_name_plural = "3 - Ustaların Fiyat Tabloları"

    def __str__(self):
        return f"{self.hesap.firma_adi} - {self.renk} Fiyatları"


# 4. PROJELER (Çizimlerin kaydedildiği depo)
class Proje(models.Model):
    hesap = models.ForeignKey(HesapProfili, on_delete=models.CASCADE, related_name='projeler', verbose_name="Çizimi Yapan Usta")
    proje_adi = models.CharField(max_length=255, verbose_name="Proje / Müşteri Adı", default="İsimsiz Proje")
    cizim_verisi = models.JSONField(verbose_name="Çizim Datası (JSON)")
    olusturulma_tarihi = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Proje"
        verbose_name_plural = "4 - Projeler"

    def __str__(self):
        return f"{self.proje_adi} - {self.hesap.firma_adi}"