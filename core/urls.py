from django.urls import path, include

from core.views import ConstructionCostPredictionAPIView, MaterialCostPredictionAPIView

urlpatterns = [
    path('predict-construction-cost', ConstructionCostPredictionAPIView.as_view(), name="predict-Cost"),
    path('predict-material-cost', MaterialCostPredictionAPIView.as_view(), name="predict-material-Cost"),
]