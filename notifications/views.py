from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from notifications.models import Notification

@login_required
def notification_list(request):
    notifications = Notification.objects.filter(user=request.user)
    unread_count = notifications.filter(is_read=False).count()
    return render(request, 'notifications/notification_list.html', {
        'notifications': notifications,
        'unread_count': unread_count
    })


@login_required
def notification_read(request, pk):
    notification = get_object_or_404(Notification, pk=pk, user=request.user)
    notification.is_read = True
    notification.save()
    return redirect('notification_list')


@login_required
def notification_read_all(request):
    Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
    messages.success(request, 'All notifications marked as read!')
    return redirect('notification_list')


@login_required
def notification_delete(request, pk):
    notification = get_object_or_404(Notification, pk=pk, user=request.user)
    notification.delete()
    messages.success(request, 'Notification deleted!')
    return redirect('notification_list')


@login_required
def notification_delete_all(request):
    Notification.objects.filter(user=request.user).delete()
    messages.success(request, 'All notifications cleared!')
    return redirect('notification_list')