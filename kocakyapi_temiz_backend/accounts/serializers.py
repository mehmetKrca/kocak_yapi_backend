from rest_framework import serializers
from .models import Proje, HesapProfili, FiyatTablosu, AbonelikPaketi

class AbonelikPaketiSerializer(serializers.ModelSerializer):
    class Meta:
        model = AbonelikPaketi
        fields = '__all__'

class HesapProfiliSerializer(serializers.ModelSerializer):
    class Meta:
        model = HesapProfili
        fields = '__all__'

class FiyatTablosuSerializer(serializers.ModelSerializer):
    class Meta:
        model = FiyatTablosu
        fields = '__all__'
        read_only_fields = ['hesap']

class ProjeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proje
        fields = '__all__'
        read_only_fields = ['hesap']