from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
from django.utils import timezone
from videos.models import (
    Video_Recommended, 
    Caster, 
    YouTubeComment, 
    CommentReply, 
    CommentSyncLog
)
import requests
from datetime import datetime, timedelta


def black_page(request):
    """หน้าหลัก - แสดง Videos, Casters และ Comments"""
    
    # ✅ ดึงข้อมูล Videos
    videos = Video_Recommended.objects.all().order_by('-id')

    # ✅ ดึงข้อมูล Casters พร้อม jobs
    casters = Caster.objects.all().prefetch_related('jobs').order_by('-created_at')
    
    # ⭐ ดึงคอมเมนท์จาก Database (ถ้ามี)
    video_id = 'cIJQrqAHpZI'  # Video ID ที่ต้องการแสดงคอมเมนท์
    
    # ตรวจสอบว่ามีคอมเมนท์ใน Database หรือไม่
    comments_qs = YouTubeComment.objects.filter(video_id=video_id).prefetch_related('replies')
    
    # ถ้าไม่มีคอมเมนท์ หรือข้อมูลเก่าเกิน 1 ชั่วโมง → ดึงจาก API
    should_sync = False
    if not comments_qs.exists():
        should_sync = True
    else:
        latest_comment = comments_qs.first()
        time_diff = timezone.now() - latest_comment.last_synced
        if time_diff > timedelta(hours=1):
            should_sync = True
    
    # ถ้าต้อง Sync → ดึงจาก YouTube API
    if should_sync:
        try:
            _sync_comments_from_youtube_silent(video_id)
            # ดึงข้อมูลใหม่หลัง Sync
            comments_qs = YouTubeComment.objects.filter(video_id=video_id).prefetch_related('replies')
        except Exception as e:
            print(f"❌ Error syncing comments: {e}")
    
    # นับจำนวนคอมเมนท์
    total_comments = comments_qs.count()

    context = {
        'videos': videos,
        'casters': casters,
        'comments': comments_qs,  # ⭐ ส่งคอมเมนท์ไปที่ Template
        'total_comments': total_comments,  # ⭐ จำนวนคอมเมนท์
        'video_id': video_id,
    }

    return render(request, 'black.html', context)


def test_images_page(request):
    """หน้าทดสอบแสดงรูปภาพ Caster"""
    casters = Caster.objects.all().prefetch_related('jobs').order_by('-created_at')

    context = {
        'casters': casters,
    }

    return render(request, 'test_images.html', context)


# ========================================
# YouTube Comments API (แบบ Cache)
# ========================================

def get_youtube_comments(request):
    """
    ⭐ API endpoint สำหรับดึง YouTube comments (แบบ Cache)
    GET /api/youtube-comments/?video_id=cIJQrqAHpZI
    GET /api/youtube-comments/?video_id=cIJQrqAHpZI&refresh=true
    GET /api/youtube-comments/?video_id=cIJQrqAHpZI&cache_hours=2
    """
    video_id = request.GET.get('video_id', 'cIJQrqAHpZI')
    force_refresh = request.GET.get('refresh', 'false').lower() == 'true'
    cache_hours = int(request.GET.get('cache_hours', 1))

    try:
        # ตรวจสอบ Cache ใน Database
        cached_comments = YouTubeComment.objects.filter(video_id=video_id)

        if cached_comments.exists() and not force_refresh:
            latest_comment = cached_comments.first()
            time_diff = timezone.now() - latest_comment.last_synced

            # ถ้าข้อมูลยังใหม่ → ใช้จาก Database
            if time_diff < timedelta(hours=cache_hours):
                return _get_comments_from_db(video_id)

        # ดึงข้อมูลจาก YouTube API
        return _sync_comments_from_youtube(video_id)

    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': 'Internal Server Error',
            'message': str(e)
        }, status=500)


def _get_comments_from_db(video_id):
    """ดึงคอมเมนท์จาก Database"""
    comments_qs = YouTubeComment.objects.filter(video_id=video_id)

    comments = []
    for comment in comments_qs:
        comment_data = {
            'id': comment.comment_id,
            'author': comment.author,
            'author_profile_image': comment.author_profile_image,
            'author_channel_url': comment.author_channel_url,
            'text': comment.text,
            'likes': comment.likes,
            'time_ago': comment.time_since_published(),
            'published_at': comment.published_at.isoformat(),
            'total_reply_count': comment.total_reply_count,
        }

        if comment.replies.exists():
            replies = []
            for reply in comment.replies.all():
                replies.append({
                    'id': reply.reply_id,
                    'author': reply.author,
                    'author_profile_image': reply.author_profile_image,
                    'text': reply.text,
                    'likes': reply.likes,
                    'time_ago': reply.time_since_published(),
                })
            comment_data['replies'] = replies

        comments.append(comment_data)

    return JsonResponse({
        'success': True,
        'video_id': video_id,
        'total_comments': comments_qs.count(),
        'comments': comments,
        'from_cache': True,
        'last_synced': comments_qs.first().last_synced.isoformat() if comments_qs.exists() else None
    })


def _sync_comments_from_youtube(video_id):
    """ดึงคอมเมนท์จาก YouTube API และบันทึกลง Database"""
    
    api_key = getattr(settings, 'YOUTUBE_API_KEY', None)
    if not api_key:
        return JsonResponse({
            'success': False,
            'error': 'YouTube API Key not configured',
            'message': 'Please add YOUTUBE_API_KEY in settings.py'
        }, status=500)

    try:
        url = 'https://www.googleapis.com/youtube/v3/commentThreads'
        params = {
            'key': api_key,
            'videoId': video_id,
            'part': 'snippet,replies',
            'maxResults': 50,
            'order': 'relevance',
            'textFormat': 'plainText'
        }

        response = requests.get(url, params=params, timeout=10)

        if response.status_code != 200:
            error_data = response.json().get('error', {})
            
            CommentSyncLog.objects.create(
                video_id=video_id,
                comments_count=0,
                success=False,
                error_message=error_data.get('message', 'Unknown error')
            )
            
            return JsonResponse({
                'success': False,
                'error': 'YouTube API Error',
                'status_code': response.status_code,
                'message': error_data.get('message', 'Unknown error')
            }, status=response.status_code)

        data = response.json()

        # ลบข้อมูลเก่าออก
        YouTubeComment.objects.filter(video_id=video_id).delete()

        # บันทึกข้อมูลใหม่
        comments_count = 0
        comments = []

        for item in data.get('items', []):
            snippet = item['snippet']['topLevelComment']['snippet']
            published_at = datetime.fromisoformat(snippet['publishedAt'].replace('Z', '+00:00'))

            comment_obj = YouTubeComment.objects.create(
                comment_id=item['id'],
                video_id=video_id,
                author=snippet['authorDisplayName'],
                author_channel_id=snippet['authorChannelId']['value'],
                author_profile_image=snippet['authorProfileImageUrl'],
                author_channel_url=snippet.get('authorChannelUrl', ''),
                text=snippet['textDisplay'],
                text_original=snippet['textOriginal'],
                likes=snippet['likeCount'],
                total_reply_count=item['snippet']['totalReplyCount'],
                published_at=published_at,
                is_public=item['snippet']['isPublic'],
                can_reply=item['snippet']['canReply'],
            )

            comments_count += 1

            reply_objects = []
            if 'replies' in item:
                for reply_item in item['replies']['comments']:
                    reply_snippet = reply_item['snippet']
                    reply_published_at = datetime.fromisoformat(
                        reply_snippet['publishedAt'].replace('Z', '+00:00')
                    )

                    reply_obj = CommentReply.objects.create(
                        reply_id=reply_item['id'],
                        parent_comment=comment_obj,
                        author=reply_snippet['authorDisplayName'],
                        author_channel_id=reply_snippet.get('authorChannelId', {}).get('value', ''),
                        author_profile_image=reply_snippet['authorProfileImageUrl'],
                        text=reply_snippet['textDisplay'],
                        likes=reply_snippet['likeCount'],
                        published_at=reply_published_at,
                    )
                    reply_objects.append(reply_obj)

            comment_data = {
                'id': comment_obj.comment_id,
                'author': comment_obj.author,
                'author_profile_image': comment_obj.author_profile_image,
                'author_channel_url': comment_obj.author_channel_url,
                'text': comment_obj.text,
                'likes': comment_obj.likes,
                'time_ago': comment_obj.time_since_published(),
                'published_at': comment_obj.published_at.isoformat(),
                'total_reply_count': comment_obj.total_reply_count,
            }

            if reply_objects:
                comment_data['replies'] = [
                    {
                        'id': r.reply_id,
                        'author': r.author,
                        'author_profile_image': r.author_profile_image,
                        'text': r.text,
                        'likes': r.likes,
                        'time_ago': r.time_since_published(),
                    }
                    for r in reply_objects
                ]

            comments.append(comment_data)

        CommentSyncLog.objects.create(
            video_id=video_id,
            comments_count=comments_count,
            success=True
        )

        return JsonResponse({
            'success': True,
            'video_id': video_id,
            'total_comments': data.get('pageInfo', {}).get('totalResults', 0),
            'comments': comments,
            'from_cache': False,
            'synced_now': True
        })

    except requests.Timeout:
        CommentSyncLog.objects.create(
            video_id=video_id,
            comments_count=0,
            success=False,
            error_message='Request Timeout'
        )
        
        return JsonResponse({
            'success': False,
            'error': 'Request Timeout',
            'message': 'YouTube API request took too long'
        }, status=504)
        
    except Exception as e:
        CommentSyncLog.objects.create(
            video_id=video_id,
            comments_count=0,
            success=False,
            error_message=str(e)
        )
        
        return JsonResponse({
            'success': False,
            'error': 'Internal Server Error',
            'message': str(e)
        }, status=500)


def _sync_comments_from_youtube_silent(video_id):
    """
    ⭐ ดึงคอมเมนท์แบบ Silent (ไม่ return JsonResponse)
    ใช้สำหรับ Sync ใน black_page()
    """
    api_key = getattr(settings, 'YOUTUBE_API_KEY', None)
    if not api_key:
        raise Exception('YouTube API Key not configured')

    url = 'https://www.googleapis.com/youtube/v3/commentThreads'
    params = {
        'key': api_key,
        'videoId': video_id,
        'part': 'snippet,replies',
        'maxResults': 50,
        'order': 'relevance',
        'textFormat': 'plainText'
    }

    response = requests.get(url, params=params, timeout=10)

    if response.status_code != 200:
        error_data = response.json().get('error', {})
        raise Exception(error_data.get('message', 'YouTube API Error'))

    data = response.json()

    # ลบข้อมูลเก่า
    YouTubeComment.objects.filter(video_id=video_id).delete()

    # บันทึกข้อมูลใหม่
    for item in data.get('items', []):
        snippet = item['snippet']['topLevelComment']['snippet']
        published_at = datetime.fromisoformat(snippet['publishedAt'].replace('Z', '+00:00'))

        comment_obj = YouTubeComment.objects.create(
            comment_id=item['id'],
            video_id=video_id,
            author=snippet['authorDisplayName'],
            author_channel_id=snippet['authorChannelId']['value'],
            author_profile_image=snippet['authorProfileImageUrl'],
            author_channel_url=snippet.get('authorChannelUrl', ''),
            text=snippet['textDisplay'],
            text_original=snippet['textOriginal'],
            likes=snippet['likeCount'],
            total_reply_count=item['snippet']['totalReplyCount'],
            published_at=published_at,
            is_public=item['snippet']['isPublic'],
            can_reply=item['snippet']['canReply'],
        )

        if 'replies' in item:
            for reply_item in item['replies']['comments']:
                reply_snippet = reply_item['snippet']
                reply_published_at = datetime.fromisoformat(
                    reply_snippet['publishedAt'].replace('Z', '+00:00')
                )

                CommentReply.objects.create(
                    reply_id=reply_item['id'],
                    parent_comment=comment_obj,
                    author=reply_snippet['authorDisplayName'],
                    author_channel_id=reply_snippet.get('authorChannelId', {}).get('value', ''),
                    author_profile_image=reply_snippet['authorProfileImageUrl'],
                    text=reply_snippet['textDisplay'],
                    likes=reply_snippet['likeCount'],
                    published_at=reply_published_at,
                )

    CommentSyncLog.objects.create(
        video_id=video_id,
        comments_count=len(data.get('items', [])),
        success=True
    )


def force_refresh_comments(request):
    """
    ⭐ Force Refresh - ลบข้อมูลเก่า + ดึงใหม่ทันที
    GET /api/youtube-comments/refresh/?video_id=cIJQrqAHpZI
    """
    video_id = request.GET.get('video_id', 'cIJQrqAHpZI')

    try:
        deleted_count = YouTubeComment.objects.filter(video_id=video_id).delete()[0]
        result = _sync_comments_from_youtube(video_id)

        if isinstance(result, JsonResponse):
            data = result.content.decode('utf-8')
            import json
            json_data = json.loads(data)
            json_data['deleted_comments'] = deleted_count
            return JsonResponse(json_data)

        return result

    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': 'Internal Server Error',
            'message': str(e)
        }, status=500)