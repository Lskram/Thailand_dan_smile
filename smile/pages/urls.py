from django.urls import path
from .views import black_page, rain_page, sakura_page

urlpatterns = [
    path('', black_page, name='black_page'),  # ✅ หน้าเว็บหลัก
    path('R/', rain_page, name='rain_page'),  # หน้า rain
    path('S/', sakura_page, name='sakura_page'),  # หน้า sakura
]
