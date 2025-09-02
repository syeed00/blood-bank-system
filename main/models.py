from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    BLOOD_GROUP_CHOICES = [
        ('O+', 'O+'),
        ('O-', 'O-'),
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True)
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES)
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.TextField(blank=True)
    last_donation_date = models.DateField(null=True, blank=True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.blood_group}"
    
    def age(self):
        if self.date_of_birth:
            from datetime import date
            today = date.today()
            return today.year - self.date_of_birth.year - (
                (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
            )
        return None

class BloodRequest(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]
    
    requested_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blood_requests')
    accepted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, 
                                   related_name='accepted_requests')
    blood_group = models.CharField(max_length=3, choices=UserProfile.BLOOD_GROUP_CHOICES)
    location = models.CharField(max_length=255)
    units_required = models.PositiveIntegerField(default=1)
    urgency = models.CharField(max_length=50, choices=[
        ('Normal', 'Normal'),
        ('Urgent', 'Urgent'),
        ('Emergency', 'Emergency'),
    ])
    message = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.blood_group} request by {self.requested_by.get_full_name()}"

class DonationHistory(models.Model):
    STATUS_CHOICES = [
        ('Scheduled', 'Scheduled'),
        ('Donated', 'Donated'),
        ('Cancelled', 'Cancelled'),
    ]
    
    donor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='donation_history')
    blood_request = models.ForeignKey(BloodRequest, on_delete=models.CASCADE, null=True, blank=True)
    donation_date = models.DateField()
    units_donated = models.PositiveIntegerField(default=1)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Scheduled')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.donor.get_full_name()} - {self.donation_date}"

# Create user profile when a new user is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()