# C:\Pro_III(DjanGo)\smile\videos\models.py
from django.db import models


# ======= แท็กประเภทวิดีโอ (ลงทะเบียนก่อน แล้วเลือกใน Video) =======
class TypeVideo(models.Model):
    slug = models.SlugField(max_length=32, unique=True)   # เช่น: cover, live, remix
    name = models.CharField(max_length=64)                # เช่น: Cover, Live, Remix

    class Meta:
        verbose_name = "ประเภทวิดีโอ"
        verbose_name_plural = "ประเภทวิดีโอ"

    def __str__(self):
        return self.name


# ======= ประเภทงาน/บทบาทของ Caster (แทน Tag_type_video เดิม) =======
class Job_type(models.Model):
    slug = models.SlugField(max_length=32, unique=True)   # เช่น: singer, dancer, reviewer
    name = models.CharField(max_length=64)                # เช่น: Singer, Dancer, Reviewer

    class Meta:
        verbose_name = "ประเภทงาน (Job)"
        verbose_name_plural = "ประเภทงาน (Job)"

    def __str__(self):
        return self.name


# ======= วิดีโอแนะนำ =======
class Video_Recommended(models.Model):
    PLATFORM_CHOICES = [
        ('Youtube', 'YouTube'),
        ('TikTok', 'TikTok'),
        ('Facebook', 'Facebook'),
    ]

    # หลัก ๆ ของวิดีโอ
    title         = models.CharField(max_length=255)                       # ชื่อเพลง/วิดีโอ
    artist        = models.CharField(max_length=255, blank=True)           # ศิลปิน (ไม่บังคับ)
    song_url      = models.URLField(blank=True, null=True)                 # ลิงก์ต้นทาง (YT/TT/FB)
    thumbnail_url = models.URLField(blank=True, null=True)                 # รูปภาพ Thumbnail
    platform      = models.CharField(
        max_length=20, choices=PLATFORM_CHOICES, blank=True, null=True
    )                                                                      # แพลตฟอร์ม

    # ✅ วีดีโอห้อยแท็ก "ประเภทวิดีโอ" ได้หลายอัน
    types         = models.ManyToManyField(TypeVideo, blank=True, related_name="videos")

    created_at    = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


# ======= โปรไฟล์คน/แคสเตอร์ =======
class Caster(models.Model):
    name          = models.CharField(max_length=255)                       # ชื่อคน
    image_url     = models.URLField(blank=True, null=True)                 # รูป
    instagram_url = models.URLField(blank=True, null=True)
    facebook_url  = models.URLField(blank=True, null=True)
    tiktok_url    = models.URLField(blank=True, null=True)

    # ✅ Caster ห้อย "Job_type" ได้หลายอัน
    jobs          = models.ManyToManyField(Job_type, blank=True, related_name="casters")

    created_at    = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name
Video = Video_Recommended