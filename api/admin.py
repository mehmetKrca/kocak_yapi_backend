from django.contrib import admin
# Mevcut modellerinin (Proje, DogramaKalemi vb.) yanına FiyatAyarlari'ni da ekle
from .models import Proje, DogramaKalemi, FiyatAyarlari 

# Eski kayıtların duruyorsa onlara dokunma, sadece en alta şunu ekle:
admin.site.register(FiyatAyarlari)