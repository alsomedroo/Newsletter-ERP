from django.contrib import admin
from .models import NewsletterUser, Newsletter

@admin.register(NewsletterUser)
class NewsletterUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_email', 'get_full_name', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'user__email', 'user__first_name', 'user__last_name')
    
    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = 'Email'
    
    def get_full_name(self, obj):
        return obj.user.get_full_name() or '-'
    get_full_name.short_description = 'Full Name'

@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'sent_at')
    list_filter = ('created_at', 'sent_at')
    search_fields = ('title', 'description')
    readonly_fields = ('created_at', 'sent_at')
    
    def has_change_permission(self, request, obj=None):
        # Prevent editing sent newsletters
        return False