from rest_framework import serializers
from .models import Proje, DogramaKalemi

class DogramaKalemiSerializer(serializers.ModelSerializer):
    class Meta:
        model = DogramaKalemi
        # proje alanını React'ten beklememesi için hariç tutuyoruz
        exclude = ['proje']
        # fiyat kısmında hata vermemesi için kuralları esnetiyoruz
        extra_kwargs = {
            'fiyat': {'required': False, 'allow_null': True}
        }

class ProjeSerializer(serializers.ModelSerializer):
    # Bu satır sayesinden bir projeyi kaydederken içindeki tüm sepet kalemleri de tek seferde kaydedilecek
    sepet_kalemleri = DogramaKalemiSerializer(many=True)

    class Meta:
        model = Proje
        fields = ['id', 'proje_adi', 'musteri_tel', 'teklif_tarihi', 'olusturma_tarihi', 'sepet_kalemleri']

    def create(self, validated_data):
        kalemler_data = validated_data.pop('sepet_kalemleri')
        proje = Proje.objects.create(**validated_data)
        for kalem_data in kalemler_data:
            DogramaKalemi.objects.create(proje=proje, **kalem_data)
        return proje