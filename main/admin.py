from django.contrib import admin
from .models import UserProfile, BloodRequest, DonationHistory

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'blood_group', 'is_available', 'last_donation_date']
    list_filter = ['blood_group', 'is_available']
    search_fields = ['user__first_name', 'user__last_name', 'user__email']

@admin.register(BloodRequest)
class BloodRequestAdmin(admin.ModelAdmin):
    list_display = ['requested_by', 'blood_group', 'location', 'urgency', 'status', 'created_at']
    list_filter = ['blood_group', 'urgency', 'status']
    search_fields = ['requested_by__first_name', 'requested_by__last_name', 'location']

@admin.register(DonationHistory)
class DonationHistoryAdmin(admin.ModelAdmin):
    list_display = ['donor', 'blood_request', 'donation_date', 'units_donated', 'status']
    list_filter = ['status', 'donation_date']
    search_fields = ['donor__first_name', 'donor__last_name']