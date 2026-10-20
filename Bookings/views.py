from django.utils import timezone
from django.db import transaction
from django.db.models import Q

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from listing.permissions import (
    landlordOrTenantPermission,
    tenantPermission,
    landlordPermission,
)

from .serializers import BookingSerializers
from .models import booking


# GET: View bookings belonging to the logged-in user
@api_view(['GET'])
@permission_classes([IsAuthenticated, landlordOrTenantPermission])
def all_bookings(request):

    if request.user.role == 'tenant':
        bookings = booking.objects.filter(tenant=request.user)

    elif request.user.role == 'landlord':
        bookings = booking.objects.filter(
            property__owner=request.user
        )

    else:
        return Response(
            {"error": "Invalid user role"},
            status=status.HTTP_403_FORBIDDEN
        )

    serializer = BookingSerializers(bookings, many=True)

    return Response(
        {"data": serializer.data},
        status=status.HTTP_200_OK
    )


# GET: View one booking by booking ID
@api_view(['GET'])
@permission_classes([IsAuthenticated, landlordOrTenantPermission])
def get_booking(request, booking_id):

    try:
        booking_obj = booking.objects.get(
            Q(tenant=request.user) |
            Q(property__owner=request.user),
            id=booking_id
        )

    except booking.DoesNotExist:
        return Response(
            {"error": "Booking not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    serializer = BookingSerializers(booking_obj)

    return Response(
        serializer.data,
        status=status.HTTP_200_OK
    )


# POST: Tenant creates a booking request
@api_view(['POST'])
@permission_classes([IsAuthenticated, tenantPermission])
def post_booking(request):

    serializer = BookingSerializers(data=request.data)

    if serializer.is_valid():
        serializer.save(
            tenant=request.user,
            status='pending'
        )

        return Response(
            {
                "message": "Booking request created successfully",
                "data": serializer.data
            },
            status=status.HTTP_201_CREATED
        )

    return Response(
        {
            "message": "Failed to create booking",
            "errors": serializer.errors
        },
        status=status.HTTP_400_BAD_REQUEST
    )


# POST: Landlord approves or rejects a booking
@api_view(['POST'])
@permission_classes([IsAuthenticated, landlordPermission])
def booking_decision(request, booking_id):

    new_status = request.data.get('status')

    if new_status not in ['approved', 'rejected']:
        return Response(
            {"error": "Status must be approved or rejected"},
            status=status.HTTP_400_BAD_REQUEST
        )

    with transaction.atomic():

        try:
            booking_obj = booking.objects.select_for_update().get(
                id=booking_id,
                property__owner=request.user
            )

        except booking.DoesNotExist:
            return Response(
                {"error": "Booking not found or not owned by you"},
                status=status.HTTP_404_NOT_FOUND
            )

        if booking_obj.status != 'pending':
            return Response(
                {"error": "Only pending bookings can be decided"},
                status=status.HTTP_400_BAD_REQUEST
            )

        booking_obj.status = new_status
        booking_obj.decided_at = timezone.now()

        booking_obj.save(
            update_fields=['status', 'decided_at']
        )

    return Response(
        {
            "message": f"Booking {new_status} successfully",
            "booking_id": booking_obj.id,
            "status": booking_obj.status,
            "decided_at": booking_obj.decided_at
        },
        status=status.HTTP_200_OK
    )