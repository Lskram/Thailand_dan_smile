from django.contrib import admin
from .models import Video

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display  = ('title', 'artist', 'url', 'created_at')
    search_fields = ('title', 'artist')
class CasterAdmin(admin.ModelAdmin):
    list_display = ("name", "instagram_url", "facebook_url", "tiktok_url")
    search_fields = ("name",)