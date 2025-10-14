from django.contrib import admin
from .models import Video

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ("title", "artist", "song_url", "thumbnail_url", "created_at")
    search_fields = ("title", "artist")
