from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    path('create-request/', views.create_blood_request, name='create_blood_request'),
    path('accept-request/<int:request_id>/', views.accept_blood_request, name='accept_blood_request'),
    path('update-donation/<int:donation_id>/', views.update_donation_status, name='update_donation_status'),
]