import joblib
import numpy as np
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from loguru import logger
from pandas import DataFrame
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

# keras load model
from keras import models
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer

# import the serializers
from core.serializer import ConstructionCostPredictionSerializer, MaterialCostPredictionSerializer

from django.shortcuts import render


def prediction_form(request):
    return render(request, 'prediction_form.html')


class ConstructionCostPredictionAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = ConstructionCostPredictionSerializer

    @csrf_exempt
    def post(self, request):
        try:
            payload = ConstructionCostPredictionSerializer(data=request.data)
            if payload.is_valid():
                # load construction prediction model from predition_models folder
                absolute_path = "core/prediction_models/construction_cost_h5_model.h5"
                model = models.load_model(absolute_path)

                # load the preprocessor from the predition_models folder
                preprocessor_path = 'core/prediction_models/preprocessor.pkl'
                preprocessor = joblib.load(preprocessor_path)

                data = payload.validated_data
                logger.info(f"Construction Cost: data -> {data}")

                # Convert data to DataFrame
                df = DataFrame(data, index=[0])
                df.columns = ['building height', 'builtup area', 'number of stories', 'number of columns',
                              'number of rooms', 'building function', 'number of units']
                logger.info(f"Construction Cost: df -> {df}")

                # Preprocess the input data
                X_preprocessed = preprocessor.transform(df)
                logger.info(f"Construction Cost: X_preprocessed -> {X_preprocessed}")

                # Make prediction
                prediction = model.predict(X_preprocessed)
                logger.info(f"Construction Cost: prediction -> {prediction[0][0]}")

                # Inverse transform the prediction if necessary (assuming log transformation was used)
                prediction_exp = np.expm1(prediction[0][0])
                logger.info(f"Construction Cost: prediction_exp -> {prediction_exp}")

                return render(request, 'prediction_result.html', {
                    'data': data,
                    'predicted_cost': float(prediction_exp)
                })
                return JsonResponse({'predicted_cost': float(prediction_exp)})
            else:
                return JsonResponse({"error": payload.errors}, status=400)
        except Exception as e:
            logger.error(f"Server Error: {str(e.with_traceback())}")
            return JsonResponse({"error": str(e)}, status=500)


class MaterialCostPredictionAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = MaterialCostPredictionSerializer

    @csrf_exempt
    def post(self, request):
        try:
            # load the bmpi_estimator model from predition_models folder
            absolute_path = "core/prediction_models/bmpi_estimator.pkl"
            model = joblib.load(absolute_path)

            payload = MaterialCostPredictionSerializer(data=request.data)
            if payload.is_valid():
                data = payload.validated_data
                logger.info(f"Material Cost: data -> {data}")

                # Convert data to DataFrame
                df = DataFrame(data, index=[0])
                df.columns = ['inflation rate', 'imports', 'exports', 'money supply m1']
                logger.info(f"Material Cost: df -> {df}")

                # Make prediction
                prediction = model.predict(df)
                logger.info(f"Material Cost: prediction -> {prediction}")

                return render(request, 'prediction_result.html', {
                    'data': data,
                    'bmpi_predicted': float(prediction[0])
                })
                return JsonResponse({'predicted_cost': float(prediction[0])})
            else:
                return JsonResponse({"error": payload.errors}, status=400)
        except Exception as e:
            logger.error(f"Server Error: {str(e.with_traceback())}")
            return JsonResponse({"error": str(e)}, status=500)
