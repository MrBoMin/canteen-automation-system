from django.urls import path
from admin import MyAdminSite
from admin_custom.admin import custom_admin_site

custom_admin_site = MyAdminSite()

urlpatterns = [
    path('admin/', custom_admin_site.urls),
]
