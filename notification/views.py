from django.http import JsonResponse
from .models import Notification

def mark_notifications_read(request):
    if request.user.is_authenticated:
        Notification.objects.filter(user=request.user, status='Unread').update(status='Read')
        return JsonResponse({'status': 'success', 'message': 'Notifications marked as read.'})
    return JsonResponse({'status': 'error', 'message': 'User not authenticated.'}, status=401)
