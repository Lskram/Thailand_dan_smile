from django.shortcuts import render
from videos.models import Video  # ✅ ดึง model จากแอป videos

def black_page(request):
    videos = Video.objects.all().order_by('-id')  # ✅ ดึงข้อมูลจากฐานข้อมูล
    context = {
        'videos': videos
    }
    return render(request, 'pages/black.html', context)
