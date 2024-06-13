from django.urls import path, include

from core.views import ConstructionCostPredictionAPIView, MaterialCostPredictionAPIView, prediction_form

urlpatterns = [
    path('', prediction_form, name='prediction_form'),
    path('predict-construction-cost', ConstructionCostPredictionAPIView.as_view(), name="predict-Cost"),
    path('predict-material-cost', MaterialCostPredictionAPIView.as_view(), name="predict-material-Cost"),
]