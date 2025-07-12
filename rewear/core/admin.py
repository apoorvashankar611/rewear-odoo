# core/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, ClothingItem, SwapRequest

# We need a custom admin view to show the 'points' field for our User
class CustomUserAdmin(UserAdmin):
    # Add 'points' to the fields shown when you view a user
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('points',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('points',)}),
    )

# This class customizes how ClothingItems are displayed
class ClothingItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'status', 'points_value', 'is_approved')
    list_filter = ('status', 'is_approved', 'category', 'condition')
    # This adds a search bar
    search_fields = ('title', 'owner__username')
    # This adds an easy way to approve items
    actions = ['approve_items']

    def approve_items(self, request, queryset):
        queryset.update(is_approved=True)
    approve_items.short_description = "Approve selected items"

# This class customizes how SwapRequests are displayed
class SwapRequestAdmin(admin.ModelAdmin):
    list_display = ('item_requested', 'requester', 'status', 'created_at')
    list_filter = ('status',)


# Register your models with the admin site
admin.site.register(User, CustomUserAdmin)
admin.site.register(ClothingItem, ClothingItemAdmin)
admin.site.register(SwapRequest, SwapRequestAdmin)