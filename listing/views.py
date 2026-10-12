from rest_framework.decorators import api_view, permission_classes
from .permissions import landlordPermission , tenantPermission , landlordOrTenantPermission
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .serializers import ListingSerializer, SavedListingSerializer
from .models import Listing, SavedListing
from rest_framework import status


@api_view(['GET'])
@permission_classes([landlordOrTenantPermission])
def get_properties(request):
    listings = Listing.objects.all()
    serializer = ListingSerializer(listings, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
@api_view(['GET'])
@permission_classes([landlordOrTenantPermission])
def get_property(request, listing_id):
    try:
        listing = Listing.objects.get(id=listing_id)
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
            return Response(
        {"message": "FAILED TO LIST","errors": serializer.errors},status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([landlordPermission])
def updatelisting(request ,pk):
    try:
        listing = Listing.objects.get(id = pk)
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
        listing = Listing.objects.get(id=pk)
    except Listing.DoesNotExist:
        return Response({'errors':'doesnt exist in database'},status=status.HTTP_404_NOT_FOUND)
    serializers = ListingSerializer(listing,data=request.data,partial=True)
    if serializers.is_valid():
        serializers.save()
    return Response(serializers.data,status = status.HTTP_200_OK)
@api_view(['DELETE'])
@permission_classes([AllowAny])
def delete_property(request, pk):
    try:
        listing = Listing.objects.get(id=pk)
    except Listing.DoesNotExist:
        return Response({"error": "Listing not found."},status=status.HTTP_404_NOT_FOUND)
    listing.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
