from django.db import models

class Video(models.Model):
    title  = models.CharField(max_length=255)
    artist = models.CharField(max_length=255, blank=True)
    url    = models.URLField(unique=True)  # ลิงก์คลิป เช่น https://www.youtube.com/watch?v=...

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
