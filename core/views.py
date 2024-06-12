from django.http import JsonResponse
from django.shortcuts import render
from loguru import logger
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView


class ConstructionPricePredictionAPIView(APIView):
    permission_classes = [AllowAny]
    # serializer_class = LoanSerializer

    def post(self, request):
        try:
            return JsonResponse({"message": "Hello World!"})
        except Exception as e:
            logger.error(f"Server Error: {str(e.with_traceback())}")
            return JsonResponse({"error": str(e)}, status=500)


class MaterialPricePredictionAPIView(APIView):
    permission_classes = [AllowAny]
    # serializer_class = LoanSerializer

    def post(self, request):
        try:
            return JsonResponse({"message": "Hello World!"})
        except Exception as e:
            logger.error(f"Server Error: {str(e.with_traceback())}")
            return JsonResponse({"error": str(e)}, status=500)

