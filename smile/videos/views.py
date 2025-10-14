# videos/views.py
from django.shortcuts import render
from django.http import JsonResponse
from .models import Video

def video_list(request):
    videos = Video.objects.all().order_by("-id")   # เปลี่ยนจาก -created_at เป็น -id
    return render(request, "videos/list.html", {"videos": videos})

def video_list_api(request):
    data = list(
        Video.objects.values("title", "artist", "url")  # เอา url ไม่ใช่ youtube_id
             .order_by("-id")[:20]
    )
    return JsonResponse(data, safe=False)
