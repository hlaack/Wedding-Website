from django.contrib import admin
from django.contrib.auth.models import User

from .models import Family, Person, RSVP_Protector


class FamilyAdmin(admin.ModelAdmin):
    """Custom admin for Family model with restricted sensitive field visibility."""
    
    list_display = ['family_name', 'familyID', 'person_count']
    list_filter = ['family_name']
    search_fields = ['family_name']
    readonly_fields = ['familyID', 'person_count']
    
    # Hide sensitive fields from list view; only show in detail view for authorized users
    fieldsets = (
        ('Family Information', {
            'fields': ('familyID', 'family_name', 'person_count')
        }),
        ('Contact Information (Restricted)', {
            'fields': ('email', 'phone_number'),
            'classes': ('collapse',)  # Collapsed by default
        }),
    )
    
    def person_count(self, obj):
        """Display number of people in family."""
        return obj.people.count()
    person_count.short_description = 'Family Size'
    
    def has_delete_permission(self, request):
        """Restrict delete permission to prevent accidental data loss."""
        return request.user.is_superuser
    
    def get_queryset(self, request):
        """Restrict queryset to prevent unauthorized access."""
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            # Non-superusers can only view (read-only)
            return qs
        return qs


class PersonAdmin(admin.ModelAdmin):
    """Custom admin for Person model with restricted sensitive field visibility."""
    
    list_display = ['first_name', 'last_name', 'associated_family', 'status', 'personID']
    list_filter = ['status', 'associated_family']
    search_fields = ['first_name', 'last_name']
    readonly_fields = ['personID']
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('personID', 'first_name', 'last_name', 'associated_family')
        }),
        ('RSVP Status', {
            'fields': ('status',)
        }),
    )
    
    def has_delete_permission(self, request):
        """Restrict delete permission to superusers only."""
        return request.user.is_superuser
    
    def get_queryset(self, request):
        """Restrict queryset to prevent unauthorized access."""
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            # Non-superusers can only view (read-only)
            return qs
        return qs


class RSVP_ProtectorAdmin(admin.ModelAdmin):
    """Custom admin for RSVP_Protector model - severely restricted access."""
    
    list_display = ['password']
    readonly_fields = ['password']  # Make password field read-only
    
    fieldsets = (
        ('RSVP Protection (Super Admin Only)', {
            'fields': ('password',),
            'classes': ('wide', 'form-row')
        }),
    )
    
    def has_add_permission(self, request):
        """Only superusers can add new password records."""
        return request.user.is_superuser
    
    def has_change_permission(self, request, obj=None):
        """Only superusers can modify password records."""
        return request.user.is_superuser
    
    def has_delete_permission(self, request):
        """Only superusers can delete password records."""
        return request.user.is_superuser
    
    def get_queryset(self, request):
        """Only superusers can view password records."""
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            return qs.none()  # Return empty queryset for non-superusers
        return qs


admin.site.register(Family, FamilyAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(RSVP_Protector, RSVP_ProtectorAdmin)
