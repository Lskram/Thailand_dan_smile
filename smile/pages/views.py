from django.shortcuts import render
from videos.models import Video_Recommended, Caster

def black_page(request):
    # ✅ ดึงข้อมูล Videos
    videos = Video_Recommended.objects.all().order_by('-id')
    
    # ✅ ดึงข้อมูล Casters พร้อม jobs (ใช้ prefetch_related เพื่อลด query)
    casters = Caster.objects.all().prefetch_related('jobs')
    # แสดงรายละเอียด Casters
    for caster in casters:
        jobs_list = [job.name for job in caster.jobs.all()]
        print(f"  - {caster.name} | Jobs: {jobs_list}")
    
    # ✅ ส่งข้อมูลทั้งคู่ไปที่ template
    context = {
        'videos': videos,
        'casters': casters,  # ✅ เพิ่มบรรทัดนี้!
    }
    
    return render(request, 'black.html', context)

def rain_page(request):
    return render(request, 'rain.html')

def sakura_page(request):
    return render(request, 'sakura.html')