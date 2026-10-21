
import logging
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .permissions import landlordPermission, tenantPermission, landlordOrTenantPermission
from .serializers import ListingSerializer, SavedListingSerializer
from .models import Listing, SavedListing
from .image_upload import upload_property_image

logger = logging.getLogger(__name__)

def get_owned_listing(request, pk):
    try:
        return Listing.objects.get(id=pk, owner=request.user)
    except Listing.DoesNotExist:
        return None

# API for getting all properties owned by the logged-in landlord
@api_view(["GET"])
@permission_classes([IsAuthenticated, landlordPermission])
def get_properties(request):
    listings = Listing.objects.filter(owner=request.user).order_by("-id")
    serializer = ListingSerializer(listings, many=True, context={"request": request})
    return Response(serializer.data, status=status.HTTP_200_OK)

# API for getting a single property
@api_view(["GET"])
@permission_classes([IsAuthenticated, landlordOrTenantPermission])
def get_property(request, listing_id):
    listing = get_owned_listing(request, listing_id)
    if listing is None:
        return Response({"error": "Listing not found or access denied"}, status=status.HTTP_404_NOT_FOUND)
    serializer = ListingSerializer(listing, context={"request": request})
    return Response(serializer.data, status=status.HTTP_200_OK)

# API for creating a property
@api_view(["POST"])
@permission_classes([IsAuthenticated, landlordPermission])
def createlisting(request):
    serializer = ListingSerializer(data=request.data, context={"request": request})
    if serializer.is_valid():
        listing = serializer.save(owner=request.user)
        return Response({"message": "Listing created successfully", "data": ListingSerializer(listing, context={"request": request}).data}, status=status.HTTP_201_CREATED)
    return Response({"message": "Failed to create listing", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

# API for updating a property completely
@api_view(["PUT"])
@permission_classes([IsAuthenticated, landlordPermission])
def updatelisting(request, pk):
    listing = get_owned_listing(request, pk)
    if listing is None:
        return Response({"error": "Listing not found or access denied"}, status=status.HTTP_404_NOT_FOUND)
    serializer = ListingSerializer(listing, data=request.data, context={"request": request})
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

# API for partially updating a property
@api_view(["PATCH"])
@permission_classes([IsAuthenticated, landlordPermission])
def updateproperty(request, pk):
    listing = get_owned_listing(request, pk)
    if listing is None:
        return Response({"error": "Listing not found or access denied"}, status=status.HTTP_404_NOT_FOUND)
    serializer = ListingSerializer(listing, data=request.data, partial=True, context={"request": request})
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

# API for deleting a property
@api_view(["DELETE"])
@permission_classes([IsAuthenticated, landlordPermission])
def delete_property(request, pk):
    listing = get_owned_listing(request, pk)
    if listing is None:
        return Response({"error": "Listing not found or access denied"}, status=status.HTTP_404_NOT_FOUND)
    listing.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

# API for uploading a property image
@api_view(["POST"])
@parser_classes([MultiPartParser, FormParser])
@permission_classes([IsAuthenticated, landlordPermission])
def upload_listing_image(request, pk):
    listing = get_owned_listing(request, pk)
    if listing is None:
        return Response({"error": "Listing not found or access denied"}, status=status.HTTP_404_NOT_FOUND)
    image_file = request.FILES.get("image")
    if not image_file:
        return Response({"error": "Image file is required"}, status=status.HTTP_400_BAD_REQUEST)
    try:
        image_url = upload_property_image(image_file)
        listing.image = image_url
        listing.save(update_fields=["image"])
        return Response({"message": "Image uploaded successfully", "listing_id": listing.id, "owner_id": listing.owner_id, "image": listing.image}, status=status.HTTP_200_OK)
    except Exception:
        logger.exception("Image upload failed for listing %s", pk)
        return Response({"error": "Image upload failed. Check server logs."}, status=status.HTTP_502_BAD_GATEWAY)

# API for tenants to browse all properties
@api_view(["GET"])
@permission_classes([IsAuthenticated, landlordOrTenantPermission])
def browse_properties(request):
    listings = Listing.objects.all().order_by("-id")
    serializer = ListingSerializer(listings, many=True, context={"request": request})
    return Response(serializer.data, status=status.HTTP_200_OK)
