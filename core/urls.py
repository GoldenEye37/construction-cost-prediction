from django.urls import path, include

from core.views import ConstructionPricePredictionAPIView, MaterialPricePredictionAPIView

urlpatterns = [
    path('predict-construction-price', ConstructionPricePredictionAPIView.as_view(), name="predict-price"),
    path('predict-material-price', MaterialPricePredictionAPIView.as_view(), name="predict-material-price"),
]