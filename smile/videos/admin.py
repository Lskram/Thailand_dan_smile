# C:\Pro_III(DjanGo)\smile\videos\admin.py
from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Video_Recommended, 
    TypeVideo, 
    Job_type, 
    Caster,
    YouTubeComment,
    CommentReply,
    CommentSyncLog
)


# ========================================
# ส่วนที่ 1: Models เดิม
# ========================================

# ---------- TypeVideo ----------
@admin.register(TypeVideo)
class TypeVideoAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    ordering = ("name",)


# ---------- Job_type ----------
@admin.register(Job_type)
class JobTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    ordering = ("name",)


# ---------- Video_Recommended ----------
@admin.register(Video_Recommended)
class VideoAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "artist",
        "platform",
        "types_list",
        "display_song_url",
        "display_thumbnail",
        "created_at",
    )
    search_fields = ("title", "artist", "song_url", "thumbnail_url")
    list_filter = ("platform", "created_at", "types")
    filter_horizontal = ("types",)
    date_hierarchy = "created_at"
    readonly_fields = ("created_at", "thumbnail_preview")
    list_per_page = 25
    ordering = ("-created_at",)

    def types_list(self, obj):
        names = [t.name for t in obj.types.all()]
        return ", ".join(names) if names else "—"
    types_list.short_description = "ประเภทวิดีโอ"

    def display_thumbnail(self, obj):
        if obj.thumbnail_url:
            return format_html('<img src="{}" width="100" />', obj.thumbnail_url)
        return "No Image"
    display_thumbnail.short_description = "Thumbnail"

    def display_song_url(self, obj):
        if obj.song_url:
            return format_html('<a href="{}" target="_blank">เปิดลิงก์</a>', obj.song_url)
        return "No URL"
    display_song_url.short_description = "Song URL"

    def thumbnail_preview(self, obj):
        if obj and obj.thumbnail_url:
            return format_html('<img src="{}" width="240" />', obj.thumbnail_url)
        return "—"
    thumbnail_preview.short_description = "Preview"


# ---------- Caster ----------
@admin.register(Caster)
class CasterAdmin(admin.ModelAdmin):
    list_display = ("name", "display_avatar", "jobs_count", "created_at")
    search_fields = ("name",)
    list_filter = ("jobs", "created_at")
    filter_horizontal = ("jobs",)
    readonly_fields = ("created_at", "avatar_preview")
    ordering = ("-created_at",)
    list_per_page = 25
    fields = (
        "name",
        "image_url",
        "avatar_preview",
        "instagram_url",
        "facebook_url",
        "tiktok_url",
        "jobs",
        "created_at",
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.prefetch_related("jobs")

    def jobs_count(self, obj):
        return obj.jobs.count()
    jobs_count.short_description = "จำนวนงาน/บทบาท"

    def display_avatar(self, obj):
        if obj.image_url:
            return format_html('<img src="{}" width="50" style="border-radius:6px;" />', obj.image_url)
        return "—"
    display_avatar.short_description = "Avatar"

    def avatar_preview(self, obj):
        if obj and obj.image_url:
            return format_html('<img src="{}" width="200" style="border-radius:10px;" />', obj.image_url)
        return "—"
    avatar_preview.short_description = "Avatar Preview"


# ========================================
# ส่วนที่ 2: YouTube Comments Models ⭐ ใหม่
# ========================================

# ---------- YouTubeComment ----------
@admin.register(YouTubeComment)
class YouTubeCommentAdmin(admin.ModelAdmin):
    """Admin panel สำหรับคอมเมนท์ YouTube"""
    
    list_display = [
        'comment_id_short',
        'video_id_short',
        'author',
        'display_avatar',
        'text_short',
        'likes',
        'total_reply_count',
        'published_at',
        'last_synced',
        'is_public',
    ]
    
    list_filter = [
        'video_id',
        'is_public',
        'is_creator',
        'is_pinned',
        'published_at',
        'last_synced',
    ]
    
    search_fields = [
        'comment_id',
        'author',
        'text',
        'video_id',
    ]
    
    readonly_fields = [
        'comment_id',
        'video_id',
        'author_channel_id',
        'published_at',
        'updated_at',
        'last_synced',
        'avatar_preview',
        'time_display',
    ]
    
    date_hierarchy = 'published_at'
    
    ordering = ['-published_at']
    
    list_per_page = 25
    
    fieldsets = (
        ('📝 ข้อมูลคอมเมนท์', {
            'fields': ('comment_id', 'video_id', 'text', 'text_original')
        }),
        ('👤 ข้อมูลผู้เขียน', {
            'fields': (
                'author', 
                'author_channel_id', 
                'author_profile_image', 
                'author_channel_url',
                'avatar_preview'
            )
        }),
        ('📊 สถิติ', {
            'fields': ('likes', 'total_reply_count')
        }),
        ('🕐 เวลา', {
            'fields': ('published_at', 'updated_at', 'last_synced', 'time_display')
        }),
        ('🚩 Flags', {
            'fields': ('is_creator', 'is_pinned', 'is_public', 'can_reply')
        }),
    )
    
    def comment_id_short(self, obj):
        """แสดง Comment ID แบบสั้น"""
        return obj.comment_id[:12] + "..."
    comment_id_short.short_description = 'Comment ID'
    
    def video_id_short(self, obj):
        """แสดง Video ID แบบสั้น"""
        return format_html(
            '<a href="https://youtube.com/watch?v={}" target="_blank">{}</a>',
            obj.video_id,
            obj.video_id[:8] + "..."
        )
    video_id_short.short_description = 'Video'
    
    def text_short(self, obj):
        """แสดงข้อความแบบสั้น"""
        return obj.text[:50] + "..." if len(obj.text) > 50 else obj.text
    text_short.short_description = 'ข้อความ'
    
    def display_avatar(self, obj):
        """แสดงรูปโปรไฟล์"""
        if obj.author_profile_image:
            return format_html(
                '<img src="{}" width="40" style="border-radius:50%;" />',
                obj.author_profile_image
            )
        return "—"
    display_avatar.short_description = 'Avatar'
    
    def avatar_preview(self, obj):
        """แสดงรูปโปรไฟล์ขนาดใหญ่"""
        if obj and obj.author_profile_image:
            return format_html(
                '<img src="{}" width="80" style="border-radius:50%;" />',
                obj.author_profile_image
            )
        return "—"
    avatar_preview.short_description = 'Preview'
    
    def time_display(self, obj):
        """แสดงเวลาแบบ relative"""
        return obj.time_since_published()
    time_display.short_description = 'เวลาที่ผ่านมา'


# ---------- CommentReply ----------
@admin.register(CommentReply)
class CommentReplyAdmin(admin.ModelAdmin):
    """Admin panel สำหรับคอมเมนท์ตอบกลับ"""
    
    list_display = [
        'reply_id_short',
        'parent_comment_short',
        'author',
        'display_avatar',
        'text_short',
        'likes',
        'published_at',
        'is_creator',
    ]
    
    list_filter = [
        'is_creator',
        'published_at',
    ]
    
    search_fields = [
        'reply_id',
        'author',
        'text',
        'parent_comment__comment_id',
    ]
    
    readonly_fields = [
        'reply_id',
        'parent_comment',
        'author_channel_id',
        'published_at',
        'updated_at',
        'avatar_preview',
        'time_display',
    ]
    
    date_hierarchy = 'published_at'
    
    ordering = ['-published_at']
    
    list_per_page = 25
    
    fieldsets = (
        ('💬 ข้อมูลคอมเมนท์ตอบกลับ', {
            'fields': ('reply_id', 'parent_comment', 'text')
        }),
        ('👤 ข้อมูลผู้เขียน', {
            'fields': (
                'author',
                'author_channel_id',
                'author_profile_image',
                'avatar_preview'
            )
        }),
        ('📊 สถิติ', {
            'fields': ('likes',)
        }),
        ('🕐 เวลา', {
            'fields': ('published_at', 'updated_at', 'time_display')
        }),
        ('🚩 Flags', {
            'fields': ('is_creator',)
        }),
    )
    
    def reply_id_short(self, obj):
        """แสดง Reply ID แบบสั้น"""
        return obj.reply_id[:12] + "..."
    reply_id_short.short_description = 'Reply ID'
    
    def parent_comment_short(self, obj):
        """แสดง Parent Comment ID"""
        return obj.parent_comment.comment_id[:12] + "..."
    parent_comment_short.short_description = 'Parent Comment'
    
    def text_short(self, obj):
        """แสดงข้อความแบบสั้น"""
        return obj.text[:50] + "..." if len(obj.text) > 50 else obj.text
    text_short.short_description = 'ข้อความ'
    
    def display_avatar(self, obj):
        """แสดงรูปโปรไฟล์"""
        if obj.author_profile_image:
            return format_html(
                '<img src="{}" width="40" style="border-radius:50%;" />',
                obj.author_profile_image
            )
        return "—"
    display_avatar.short_description = 'Avatar'
    
    def avatar_preview(self, obj):
        """แสดงรูปโปรไฟล์ขนาดใหญ่"""
        if obj and obj.author_profile_image:
            return format_html(
                '<img src="{}" width="80" style="border-radius:50%;" />',
                obj.author_profile_image
            )
        return "—"
    avatar_preview.short_description = 'Preview'
    
    def time_display(self, obj):
        """แสดงเวลาแบบ relative"""
        return obj.time_since_published()
    time_display.short_description = 'เวลาที่ผ่านมา'


# ---------- CommentSyncLog ----------
@admin.register(CommentSyncLog)
class CommentSyncLogAdmin(admin.ModelAdmin):
    """Admin panel สำหรับ Sync Log"""
    
    list_display = [
        'status_icon',
        'video_id_link',
        'synced_at',
        'comments_count',
        'success',
        'error_short',
    ]
    
    list_filter = [
        'success',
        'synced_at',
    ]
    
    search_fields = [
        'video_id',
        'error_message',
    ]
    
    readonly_fields = [
        'video_id',
        'synced_at',
        'comments_count',
        'success',
        'error_message',
    ]
    
    date_hierarchy = 'synced_at'
    
    ordering = ['-synced_at']
    
    list_per_page = 50
    
    def has_add_permission(self, request):
        """ไม่อนุญาตให้เพิ่ม Log ด้วยตนเอง"""
        return False
    
    def status_icon(self, obj):
        """แสดงไอคอนสถานะ"""
        if obj.success:
            return format_html('<span style="font-size:20px;">✅</span>')
        return format_html('<span style="font-size:20px;">❌</span>')
    status_icon.short_description = 'Status'
    
    def video_id_link(self, obj):
        """แสดง Video ID พร้อมลิงก์"""
        return format_html(
            '<a href="https://youtube.com/watch?v={}" target="_blank">{}</a>',
            obj.video_id,
            obj.video_id
        )
    video_id_link.short_description = 'Video ID'
    
    def error_short(self, obj):
        """แสดง Error Message แบบสั้น"""
        if obj.error_message:
            return obj.error_message[:50] + "..." if len(obj.error_message) > 50 else obj.error_message
        return "—"
    error_short.short_description = 'Error Message'