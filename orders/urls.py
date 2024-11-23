from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('cart/add/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_view, name='cart'),
    path('cart/update/<int:item_id>/', views.update_cart_item, name='update_cart_item'),
    path('cart/remove/<int:item_id>/', views.remove_cart_item, name='remove_cart_item'),
    path('summary/<int:order_id>/', views.order_summary_view, name='order_summary'),
    path('make_order', views.make_order, name='make_order')
]
