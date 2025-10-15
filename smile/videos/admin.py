# C:\Pro_III(DjanGo)\smile\videos\admin.py
from django.contrib import admin
from django.utils.html import format_html
from .models import Video_Recommended, TypeVideo, Job_type, Caster


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
        "types_list",           # แสดงรายชื่อประเภทวิดีโอ
        "display_song_url",     # ลิงก์เพลง
        "display_thumbnail",    # รูป thumbnail
        "created_at",
    )
    search_fields = ("title", "artist", "song_url", "thumbnail_url")
    list_filter = ("platform", "created_at", "types")
    filter_horizontal = ("types",)  # ✅ เลือกหลายแท็กได้ง่าย
    date_hierarchy = "created_at"
    readonly_fields = ("created_at", "thumbnail_preview")
    list_per_page = 25
    ordering = ("-created_at",)

    # แสดงรายชื่อประเภทวิดีโอใน list
    def types_list(self, obj):
        names = [t.name for t in obj.types.all()]
        return ", ".join(names) if names else "—"
    types_list.short_description = "ประเภทวิดีโอ"

    # แสดงรูปในหน้า list
    def display_thumbnail(self, obj):
        if obj.thumbnail_url:
            return format_html('<img src="{}" width="100" />', obj.thumbnail_url)
        return "No Image"
    display_thumbnail.short_description = "Thumbnail"

    # แสดงลิงก์เพลงในหน้า list
    def display_song_url(self, obj):
        if obj.song_url:
            return format_html('<a href="{}" target="_blank">เปิดลิงก์</a>', obj.song_url)
        return "No URL"
    display_song_url.short_description = "Song URL"

    # พรีวิวรูปในหน้าแก้ไขฟอร์ม
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
    filter_horizontal = ("jobs",)  # ✅ เลือกหลาย Job ได้ง่าย
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
