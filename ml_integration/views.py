
import requests

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .serializers import RentPredictionSerializer
from .services import call_ml_model


def forward_to_ml(endpoint, payload):
    try:
        result = call_ml_model(endpoint, payload)
        return Response(result, status=status.HTTP_200_OK)

    except requests.HTTPError as exc:
        upstream = exc.response
        return Response(
            {
                "success": False,
                "message": "ML service rejected the request",
                "ml_status": upstream.status_code,
                "details": upstream.text[:2000],
            },
            status=status.HTTP_502_BAD_GATEWAY,
        )

    except (requests.RequestException, ValueError) as exc:
        return Response(
            {
                "success": False,
                "message": "Unable to get a response from ML service",
                "details": str(exc),
            },
            status=status.HTTP_502_BAD_GATEWAY,
        )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def predict_rent(request):
    serializer = RentPredictionSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )

    return forward_to_ml(
        "/predict-rent",
        serializer.validated_data,
    )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def check_listing(request):
    if not isinstance(request.data, dict):
        return Response(
            {"message": "Send a JSON object"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    return forward_to_ml("/check-listing", request.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def recommend_homes(request):
    if not isinstance(request.data, dict):
        return Response(
            {"message": "Send a JSON object"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    return forward_to_ml("/recommend-homes", request.data)
