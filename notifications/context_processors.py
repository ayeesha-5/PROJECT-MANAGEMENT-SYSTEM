from notifications.models import Notification


def unread_notifications(request):
    """
    Injects unread_notifications count into every template automatically.
    This fixes the sidebar bell badge showing 0 or crashing on all pages.
    """
    if request.user.is_authenticated:
        count = Notification.objects.filter(
            user=request.user, is_read=False
        ).count()
        return {'unread_notifications': count}
    return {'unread_notifications': 0}
