from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.auth import get_user_model

User = get_user_model()


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    action = models.CharField(max_length=50)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")
    time_sent = models.DateTimeField(auto_now_add=True)
    is_showed = models.BooleanField(default=False)

    class Meta:
        ordering = ["-time_sent"]
        indexes = [
            models.Index(fields=['user', '-time_sent']),
        ]

