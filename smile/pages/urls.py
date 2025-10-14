from django.urls import path
from .views import black_page

urlpatterns = [
    path('', black_page, name='black_page'),  # ✅ หน้าเว็บหลัก
]
