# C:\Pro_III(DjanGo)\smile\videos\models.py
from django.db import models
from django.utils import timezone


# ========================================
# ส่วนที่ 1: Models เดิม (Video & Caster)
# ========================================

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
        verbose_name = "วิดีโอแนะนำ"
        verbose_name_plural = "วิดีโอแนะนำ"

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
        verbose_name = "Caster"
        verbose_name_plural = "Casters"

    def __str__(self):
        return self.name


# Alias สำหรับใช้งาน
Video = Video_Recommended


# ========================================
# ส่วนที่ 2: Models ใหม่ (YouTube Comments)
# ========================================

class YouTubeComment(models.Model):
    """
    ⭐ Model สำหรับเก็บคอมเมนท์จาก YouTube
    """
    # Primary Key
    comment_id = models.CharField(max_length=255, unique=True, primary_key=True)
    
    # Video Info
    video_id = models.CharField(max_length=100, db_index=True)
    
    # Author Info
    author = models.CharField(max_length=255)
    author_channel_id = models.CharField(max_length=100)
    author_profile_image = models.URLField(max_length=500)
    author_channel_url = models.URLField(max_length=500, blank=True)
    
    # Comment Content
    text = models.TextField()
    text_original = models.TextField()
    
    # Statistics
    likes = models.IntegerField(default=0)
    total_reply_count = models.IntegerField(default=0)
    
    # Timestamps
    published_at = models.DateTimeField()
    updated_at = models.DateTimeField(auto_now=True)
    last_synced = models.DateTimeField(auto_now=True)
    
    # Flags
    is_creator = models.BooleanField(default=False)
    is_pinned = models.BooleanField(default=False)
    is_public = models.BooleanField(default=True)
    can_reply = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-published_at']
        verbose_name = 'YouTube Comment'
        verbose_name_plural = 'YouTube Comments'
        indexes = [
            models.Index(fields=['video_id', '-published_at']),
            models.Index(fields=['video_id', '-likes']),
            models.Index(fields=['-last_synced']),
        ]
    
    def __str__(self):
        return f"{self.author}: {self.text[:50]}..."
    
    def time_since_published(self):
        """คำนวณเวลาที่ผ่านไป"""
        now = timezone.now()
        diff = now - self.published_at
        seconds = diff.total_seconds()
        
        if seconds < 60:
            return "เมื่อสักครู่"
        elif seconds < 3600:
            minutes = int(seconds / 60)
            return f"{minutes} นาทีที่ผ่านมา"
        elif seconds < 86400:
            hours = int(seconds / 3600)
            return f"{hours} ชั่วโมงที่ผ่านมา"
        elif seconds < 604800:
            days = int(seconds / 86400)
            return f"{days} วันที่ผ่านมา"
        elif seconds < 2592000:
            weeks = int(seconds / 604800)
            return f"{weeks} สัปดาห์ที่ผ่านมา"
        elif seconds < 31536000:
            months = int(seconds / 2592000)
            return f"{months} เดือนที่ผ่านมา"
        else:
            years = int(seconds / 31536000)
            return f"{years} ปีที่ผ่านมา"
    
    def is_stale(self, hours=1):
        """ตรวจสอบว่าข้อมูลเก่าเกินไปหรือไม่"""
        from datetime import timedelta
        time_diff = timezone.now() - self.last_synced
        return time_diff.total_seconds() > (hours * 3600)


class CommentReply(models.Model):
    """
    ⭐ Model สำหรับเก็บคอมเมนท์ตอบกลับ
    """
    # Primary Key
    reply_id = models.CharField(max_length=255, unique=True, primary_key=True)
    
    # Foreign Key
    parent_comment = models.ForeignKey(
        YouTubeComment,
        on_delete=models.CASCADE,
        related_name='replies'
    )
    
    # Author Info
    author = models.CharField(max_length=255)
    author_channel_id = models.CharField(max_length=100, blank=True)
    author_profile_image = models.URLField(max_length=500)
    
    # Content
    text = models.TextField()
    likes = models.IntegerField(default=0)
    
    # Timestamps
    published_at = models.DateTimeField()
    updated_at = models.DateTimeField(auto_now=True)
    
    # Flags
    is_creator = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['published_at']
        verbose_name = 'Comment Reply'
        verbose_name_plural = 'Comment Replies'
    
    def __str__(self):
        return f"Reply by {self.author} on {self.parent_comment.comment_id[:8]}..."
    
    def time_since_published(self):
        """คำนวณเวลาที่ผ่านไป"""
        now = timezone.now()
        diff = now - self.published_at
        seconds = diff.total_seconds()
        
        if seconds < 60:
            return "เมื่อสักครู่"
        elif seconds < 3600:
            minutes = int(seconds / 60)
            return f"{minutes} นาทีที่ผ่านมา"
        elif seconds < 86400:
            hours = int(seconds / 3600)
            return f"{hours} ชั่วโมงที่ผ่านมา"
        elif seconds < 604800:
            days = int(seconds / 86400)
            return f"{days} วันที่ผ่านมา"
        elif seconds < 2592000:
            weeks = int(seconds / 604800)
            return f"{weeks} สัปดาห์ที่ผ่านมา"
        elif seconds < 31536000:
            months = int(seconds / 2592000)
            return f"{months} เดือนที่ผ่านมา"
        else:
            years = int(seconds / 31536000)
            return f"{years} ปีที่ผ่านมา"


class CommentSyncLog(models.Model):
    """
    ⭐ Model สำหรับบันทึกประวัติการ Sync คอมเมนท์จาก YouTube API
    """
    video_id = models.CharField(max_length=100)
    synced_at = models.DateTimeField(auto_now_add=True)
    comments_count = models.IntegerField(default=0)
    success = models.BooleanField(default=True)
    error_message = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-synced_at']
        verbose_name = 'Sync Log'
        verbose_name_plural = 'Sync Logs'
    
    def __str__(self):
        status = "✅" if self.success else "❌"
        return f"{status} {self.video_id} - {self.synced_at.strftime('%Y-%m-%d %H:%M')}"


# ========================================
# สรุป Models ทั้งหมด
# ========================================
# 1. TypeVideo - ประเภทวิดีโอ (Cover, Live, Remix, ...)
# 2. Job_type - ประเภทงาน (Singer, Dancer, Reviewer, ...)
# 3. Video_Recommended (alias: Video) - วิดีโอแนะนำ
# 4. Caster - โปรไฟล์คน/แคสเตอร์
# 5. YouTubeComment - คอมเมนท์จาก YouTube ⭐ ใหม่
# 6. CommentReply - คอมเมนท์ตอบกลับ ⭐ ใหม่
# 7. CommentSyncLog - ประวัติการ Sync ⭐ ใหม่