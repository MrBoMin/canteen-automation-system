from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls import handler404
from django.urls import path, include
from django.contrib import admin
from django.conf.urls import handler404
from canteen_automation.views import custom_404

handler404 = 'canteen_automation.views.custom_404'


urlpatterns = [
    path('admin/', admin.site.urls),  # Use your custom admin site
    path('', include('pages.urls')),
    path('users/', include('users.urls')),
    path('menu/', include('menu.urls')),  # Include menu app URLs
    path('orders/', include('orders.urls', namespace='orders')),
    path('notification/', include('notification.urls')),
    path('payments/', include('payments.urls')),
]



if settings.DEBUG:  # Only apply this in DEBUG mode (development)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
