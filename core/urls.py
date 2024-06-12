from django.urls import path, include

from core.views import ConstructionPricePredictionAPIView

urlpatterns = [
    path('predict', ConstructionPricePredictionAPIView.as_view(), name="predict-price"),
]