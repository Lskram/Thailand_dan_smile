from django.urls import path
from .views import (
    black_page, 
    test_images_page, 
    get_youtube_comments,
    force_refresh_comments
)

urlpatterns = [
    # ========================================
    # หน้าเว็บ (Pages)
    # ========================================
    path('', black_page, name='black_page'),  
    # ✅ หน้าเว็บหลัก
    
    path('test-images/', test_images_page, name='test_images'),  
    # 🔍 หน้าทดสอบรูปภาพ Caster
    
    
    # ========================================
    # API Endpoints
    # ========================================
    path('api/youtube-comments/', get_youtube_comments, name='youtube_comments'),  
    # 💬 ดึงคอมเมนท์ (มี Cache)
    # GET /api/youtube-comments/?video_id=cIJQrqAHpZI
    # GET /api/youtube-comments/?video_id=cIJQrqAHpZI&cache_hours=2
    # GET /api/youtube-comments/?video_id=cIJQrqAHpZI&refresh=true
    
    path('api/youtube-comments/refresh/', force_refresh_comments, name='force_refresh_comments'),
    # ⚡ Force Refresh (ลบข้อมูลเก่า + ดึงใหม่)
    # GET /api/youtube-comments/refresh/?video_id=cIJQrqAHpZI
]


# ========================================
# วิธีเรียกใช้ API
# ========================================

# 1. ดึงคอมเมนท์ปกติ (จะใช้ Cache ถ้ามี):
#    http://localhost:8000/api/youtube-comments/?video_id=cIJQrqAHpZI

# 2. ดึงคอมเมนท์ (Cache 2 ชั่วโมง):
#    http://localhost:8000/api/youtube-comments/?video_id=cIJQrqAHpZI&cache_hours=2

# 3. ดึงคอมเมนท์ใหม่ทันที (ไม่ใช้ Cache):
#    http://localhost:8000/api/youtube-comments/?video_id=cIJQrqAHpZI&refresh=true

# 4. Force Refresh (ลบข้อมูลเก่าทั้งหมด + ดึงใหม่):
#    http://localhost:8000/api/youtube-comments/refresh/?video_id=cIJQrqAHpZI