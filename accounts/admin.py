from django.contrib import admin
from django import forms
from django.contrib.auth.models import User, Group
from .models import AbonelikPaketi, HesapProfili, FiyatTablosu

# 1. Gereksiz Gruplar menüsünü gizliyoruz
admin.site.unregister(Group)

# 2. Abonelik Paketleri Görünümü
@admin.register(AbonelikPaketi)
class AbonelikPaketiAdmin(admin.ModelAdmin):
    list_display = ('paket_adi', 'aylik_fiyat')

# --- Fiyat Tablosunu Müşterinin İçine Gömme (Inline) ---
class FiyatTablosuInline(admin.TabularInline):
    model = FiyatTablosu
    extra = 0

# 3. ŞİPŞAK MÜŞTERİ EKLEME FORMU 
class HesapProfiliForm(forms.ModelForm):
    kullanici_adi = forms.CharField(max_length=150, required=False, label="Sisteme Giriş Adı (Yeni Kayıt İçin)")
    sifre = forms.CharField(max_length=150, required=False, label="Giriş Şifresi (Yeni Kayıt İçin)")

    class Meta:
        model = HesapProfili
        exclude = ['user']

    def clean(self):
        cleaned_data = super().clean()
        k_adi = cleaned_data.get('kullanici_adi')
        sif = cleaned_data.get('sifre')
        
        # Sadece yeni kayıt eklenirken çalışacak kontroller
        if not self.instance.pk: 
            # 1. Boş bırakıldı mı kontrolü
            if not k_adi or not sif:
                raise forms.ValidationError("Yeni usta eklerken Kullanıcı Adı ve Şifre girmelisiniz!")
            
            # 2. SİHİRLİ DOKUNUŞ: Bu kullanıcı adı daha önce alınmış mı kontrolü!
            if User.objects.filter(username=k_adi).exists():
                self.add_error('kullanici_adi', "Bu Kullanıcı Adı zaten sistemde var! Lütfen farklı bir isim girin (Örn: ahmet_usta_2)")
                
        return cleaned_data

    def save(self, commit=True):
        profil = super().save(commit=False)
        yeni_kayit_mi = False 
        
        if not profil.pk:
            k_adi = self.cleaned_data.get('kullanici_adi')
            sif = self.cleaned_data.get('sifre')
            yeni_user = User.objects.create_user(username=k_adi, password=sif)
            profil.user = yeni_user
            yeni_kayit_mi = True 
        
        if commit:
            profil.save()
            if yeni_kayit_mi:
                renkler = ['beyaz', 'antrasit', 'altin_mese']
                for r in renkler:
                    FiyatTablosu.objects.create(hesap=profil, renk=r)
                    
        return profil

# 4. PATRON KOKPİTİ
@admin.register(HesapProfili)
class HesapProfiliAdmin(admin.ModelAdmin):
    form = HesapProfiliForm
    list_display = ('firma_adi', 'telefon', 'paket', 'aktif_mi')
    list_editable = ('aktif_mi',)
    list_filter = ('aktif_mi', 'paket')
    search_fields = ('firma_adi', 'telefon')
    inlines = [FiyatTablosuInline]