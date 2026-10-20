from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_bookings, name='all-bookings'),
    path('create/', views.post_booking, name='create-booking'),
    path('<int:booking_id>/', views.get_booking, name='get-booking'),
    path(
        '<int:booking_id>/decision/',
        views.booking_decision,
        name='booking-decision'
    ),
]