from rest_framework.decorators import api_view, permission_classes
from .permissions import landlordPermission , tenantPermission , landlordOrTenantPermission
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .serializers import ListingSerializer, SavedListingSerializer
from .models import Listing, SavedListing
from rest_framework import status
from .image_upload import upload_property_image
from rest_framework.permissions import IsAuthenticated
def get_owned_listing(request, pk):
    try:
        return Listing.objects.get(
            id=pk,
            owner=request.user
        )
    except Listing.DoesNotExist:
        return None
@api_view(['GET'])

@api_view(['GET'])
@permission_classes([IsAuthenticated, landlordPermission])
def get_properties(request):
    listings = Listing.objects.filter(owner=request.user)

    serializer = ListingSerializer(listings, many=True)

    return Response(serializer.data,status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([landlordOrTenantPermission])
def get_property(request, listing_id):
    try:
        listing = Listing.objects.get(id=listing_id,owner=request.user)
    except Listing.DoesNotExist:
        return Response({'error': 'Listing not found'}, status=status.HTTP_400_BAD_REQUEST)

    serializer = ListingSerializer(listing)
    return Response(serializer.data, status=200)
@api_view(['POST'])
@permission_classes([landlordPermission])
def createlisting(request):
    serializer = ListingSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(owner=request.user)
        return Response({"message":"LISTED SUCESS","data":serializer.data},status=status.HTTP_201_CREATED)
    else:
            return Response({"message": "FAILED TO LIST","errors": serializer.errors},status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([landlordPermission])
def updatelisting(request ,pk):
    try:
        listing = Listing.objects.get(id = pk,owner=request.user)
    except Listing.DoesNotExist:
        return Response({'error':'listingNOTexist'},status=status.HTTP_400_BAD_REQUEST)
    serializer = ListingSerializer(listing,data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data,status=status.HTTP_200_OK)
    return Response({'errors':serializer.errors},status=status.HTTP_400_BAD_REQUEST)
@api_view(['PATCH'])
@permission_classes([landlordPermission])
def updateproperty(request,pk):
    try:
        listing = Listing.objects.get(id=pk,owner=request.user)
    except Listing.DoesNotExist:
        return Response({'errors':'doesnt exist in database'},status=status.HTTP_404_NOT_FOUND)
    serializers = ListingSerializer(listing,data=request.data,partial=True)
    if serializers.is_valid():
        serializers.save()
        return Response(serializers.data,status = status.HTTP_200_OK)
@api_view(['DELETE'])

@api_view(['DELETE'])
@permission_classes([IsAuthenticated, landlordPermission])
def delete_property(request, pk):
    try:
        listing = Listing.objects.get(
            id=pk,
            owner=request.user
        )
    except Listing.DoesNotExist:
        return Response(
            {"error": "Listing not found or access denied"},
            status=status.HTTP_404_NOT_FOUND
        )

    listing.delete()

    return Response(status=status.HTTP_204_NO_CONTENT)

import logging

from rest_framework.decorators import (
    api_view,
    permission_classes,
    parser_classes,
)
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

logger = logging.getLogger(__name__)


@api_view(["POST"])
@parser_classes([MultiPartParser, FormParser])
@permission_classes([IsAuthenticated, landlordPermission])
def upload_listing_image(request, pk):
    listing = get_owned_listing(request, pk)

    if listing is None:
        return Response(
            {"error": "Listing not found or access denied"},
            status=status.HTTP_404_NOT_FOUND,
        )

    image_file = request.FILES.get("image")

    if not image_file:
        return Response(
            {"error": "Image file is required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        image_url = upload_property_image(image_file)

        listing.image = image_url
        listing.save(update_fields=["image"])

        return Response(
            {
                "message": "Image uploaded successfully",
                "listing_id": listing.id,
                "owner_id": listing.owner_id,
                "image": listing.image,
            },
            status=status.HTTP_200_OK,
        )

    except Exception:
        logger.exception("Cloudinary upload failed for listing %s", pk)

        return Response(
            {"error": "Image upload failed. Check server logs."},
            status=status.HTTP_502_BAD_GATEWAY,
        )