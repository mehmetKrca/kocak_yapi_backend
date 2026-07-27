from django.db import models

class Proje(models.Model):
    proje_adi = models.CharField(max_length=200, verbose_name="Proje / Müşteri Adı")
    musteri_tel = models.CharField(max_length=50, blank=True, null=True, verbose_name="Müşteri Telefonu")
    teklif_tarihi = models.CharField(max_length=50, verbose_name="Teklif Tarihi")
    olusturma_tarihi = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.proje_adi

class DogramaKalemi(models.Model):
    # Bu satır, bu pencerenin hangi projeye ait olduğunu bağlıyor
    proje = models.ForeignKey(Proje, related_name='sepet_kalemleri', on_delete=models.CASCADE)
    
    kalem_adi = models.CharField(max_length=150, verbose_name="Oda / Kalem Adı")
    urun_tipi = models.CharField(max_length=50, verbose_name="Ürün Tipi")
    genislik = models.IntegerField(verbose_name="Genişlik (mm)")
    yukseklik = models.IntegerField(verbose_name="Yükseklik (mm)")
    sag_yukseklik = models.IntegerField(default=1600, verbose_name="Sağ Boy (Açılı için)")
    bolme_sayisi = models.IntegerField(default=1, verbose_name="Bölme Sayısı")
    
    # Kanat dizilimlerini ve özel ölçüleri metin (JSON) olarak saklayacağız ki esnek olsun
    kanatlar = models.JSONField(default=list, verbose_name="Kanat Tipleri")
    bolme_olculeri = models.JSONField(default=list, verbose_name="Asimetrik Ölçüler")
    
    renk = models.CharField(max_length=50, verbose_name="Profil Rengi")
    cam_tipi = models.CharField(max_length=50, verbose_name="Cam Tipi")
    sineklik_iste = models.BooleanField(default=False, verbose_name="Sineklik Var mı")
    alt_panel_lambiri = models.BooleanField(default=True, verbose_name="Alt Lambiri Var mı")
    
    fiyat = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Kalem Fiyatı (TL)")

    def __str__(self):
        return f"{self.proje.proje_adi} - {self.kalem_adi} ({self.fiyat} TL)"
class FiyatAyarlari(models.Model):
    RENK_SECENEKLERI = [
        ('beyaz', 'Beyaz'),
        ('antrasit', 'Antrasit Gri'),
        ('altin_mese', 'Altın Meşe'),
    ]
    renk = models.CharField(max_length=20, choices=RENK_SECENEKLERI, default='beyaz')

    # --- UPVC PROFİLLERİ (m) ---
    upvc_kasa = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    upvc_ortakayit = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    upvc_pencere_kanadi = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    upvc_kapi_kanadi = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    upvc_surme_kasa = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    upvc_surme_kanadi = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    # --- ALÜMİNYUM PROFİLLERİ (m) ---
    al_kasa = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    al_ortakayit = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    al_pencere_kanadi = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    al_kapi_kanadi = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    al_surme_kasa = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    al_surme_kanadi = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    # --- AKSESUARLAR (Sayı) ---
    aksesuar_tek_acilim = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    aksesuar_cift_acilim = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    aksesuar_vasistas = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    aksesuar_kapi = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    aksesuar_surme = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    # --- CAM VE LAMBİRİ (m²) & CAM İÇİ ALANLAR ---
    cam_fiyati = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    cam_ici_detay = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    upvc_lambiri = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    aluminyum_lambiri = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    # --- DİĞER ---
    kdv_orani = models.DecimalField(max_digits=5, decimal_places=2, default=20)
    para_birimi = models.CharField(max_length=10, default='TL')
    ondalik_basamak = models.IntegerField(default=0)

    def __str__(self):
        return f"Fiyat Ayarları - {self.get_renk_display()}"