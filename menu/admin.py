from django.contrib import admin
from .models import MenuItem, Category, Review

admin.site.register(Category)
admin.site.register(MenuItem)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'menu_item', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('user__username', 'menu_item__item_name', 'comment')