# videos/models.py
from django.db import models

class Video(models.Model):
    PLATFORM_CHOICES = [
        ('youtube', 'YouTube'),
        ('tiktok', 'TikTok'),
        ('facebook', 'Facebook'),
    ]

    title = models.CharField(max_length=255)                         # ชื่อเพลง
    artist = models.CharField(max_length=255)                        # ศิลปิน
    song_url = models.URLField(blank=True, null=True)               # ลิงก์เพลง
    thumbnail_url = models.URLField(blank=True, null=True)          # ลิงก์รูปภาพ
    platform = models.CharField(                                     # ✅ เพิ่มฟิลด์นี้
        max_length=20,
        choices=PLATFORM_CHOICES,
        default='youtube'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.artist}"
