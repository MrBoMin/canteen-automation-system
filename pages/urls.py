from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),  # Home page at root URL
    path('header.html', views.header_view, name='header'),
    path('footer.html', views.footer_view, name='footer'),
    path('about', views.about_view, name='about'),
    path('contact', views.contact_view, name='contact')
]
