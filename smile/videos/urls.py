from django.urls import path
from .views import video_list, video_list_api

urlpatterns = [
    path("", video_list, name="video_list"),
    path("api/list/", video_list_api, name="video_list_api"),
]
