from django.contrib import admin
from .models import MenuItem, Category, Review

admin.site.register(Category)


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('item_name', 'price', 'category','stock')  # Removed is_available
    list_filter = ('category',)  # Removed is_available
    search_fields = ('item_name', 'category__name')
    ordering = ('item_name',)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'menu_item', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('user__username', 'menu_item__item_name', 'comment')