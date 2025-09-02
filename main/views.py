from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.db.models import Q

from .forms import UserRegistrationForm, UserProfileForm, BloodRequestForm, DonationHistoryForm
from .models import UserProfile, BloodRequest, DonationHistory

def home(request):
    # Get all available donors
    donors = UserProfile.objects.filter(is_available=True)
    
    # Handle search and filter
    blood_group = request.GET.get('blood_group')
    search_query = request.GET.get('search')
    
    if blood_group:
        donors = donors.filter(blood_group=blood_group)
    
    if search_query:
        donors = donors.filter(
            Q(user__first_name__icontains=search_query) |
            Q(user__last_name__icontains=search_query) |
            Q(address__icontains=search_query)
        )
    
    # Pagination
    paginator = Paginator(donors, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'blood_groups': UserProfile.BLOOD_GROUP_CHOICES,
    }
    return render(request, 'main/home.html', context)

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # In a real application, you would send an email verification link here
            # For this example, we'll just activate the user directly
            user.is_active = True
            user.save()
            
            messages.success(request, 'Your account has been created! You can now log in.')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'main/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            if user.is_active:
                login(request, user)
                messages.success(request, f'Welcome back, {user.get_full_name()}!')
                return redirect('dashboard')
            else:
                messages.error(request, 'Your account is not active. Please verify your email.')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'main/login.html')

def user_logout(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('home')

@login_required
def dashboard(request):
    user_profile = UserProfile.objects.get(user=request.user)
    
    # Get blood requests (excluding those created by the current user)
    blood_requests = BloodRequest.objects.exclude(requested_by=request.user).filter(status='Pending')
    
    # Get user's donation history
    donation_history = DonationHistory.objects.filter(donor=request.user)
    
    context = {
        'user_profile': user_profile,
        'blood_requests': blood_requests,
        'donation_history': donation_history,
    }
    return render(request, 'main/dashboard.html', context)

@login_required
def profile(request):
    user_profile = UserProfile.objects.get(user=request.user)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=user_profile)
    
    return render(request, 'main/profile.html', {'form': form})

@login_required
def create_blood_request(request):
    if request.method == 'POST':
        form = BloodRequestForm(request.POST)
        if form.is_valid():
            blood_request = form.save(commit=False)
            blood_request.requested_by = request.user
            blood_request.save()
            messages.success(request, 'Your blood request has been created!')
            return redirect('dashboard')
    else:
        form = BloodRequestForm()
    
    return render(request, 'main/create_blood_request.html', {'form': form})

@login_required
def accept_blood_request(request, request_id):
    blood_request = get_object_or_404(BloodRequest, id=request_id)
    
    if request.method == 'POST':
        # Update blood request status
        blood_request.accepted_by = request.user
        blood_request.status = 'Accepted'
        blood_request.save()
        
        # Create donation history record
        DonationHistory.objects.create(
            donor=request.user,
            blood_request=blood_request,
            donation_date=None,  # Will be updated later
            status='Scheduled',
            notes=f"Accepted blood request from {blood_request.requested_by.get_full_name()}"
        )
        
        messages.success(request, f'You have accepted the blood request for {blood_request.blood_group}.')
        return redirect('dashboard')
    
    return render(request, 'main/accept_blood_request.html', {'blood_request': blood_request})

@login_required
def update_donation_status(request, donation_id):
    donation = get_object_or_404(DonationHistory, id=donation_id, donor=request.user)
    
    if request.method == 'POST':
        form = DonationHistoryForm(request.POST, instance=donation)
        if form.is_valid():
            form.save()
            messages.success(request, 'Donation status updated!')
            return redirect('dashboard')
    else:
        form = DonationHistoryForm(instance=donation)
    
    return render(request, 'main/update_donation_status.html', {'form': form, 'donation': donation})