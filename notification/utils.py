from .models import Notification


def create_notification(user, action, content_object):
    try:
        Notification.objects.create(user=user, action=action, content_object=content_object)
        return True
    except ValueError:
        return False
