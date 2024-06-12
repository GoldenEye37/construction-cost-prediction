import joblib
import numpy as np
from django.http import JsonResponse
from django.shortcuts import render
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


class ConstructionCostPredictionAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = ConstructionCostPredictionSerializer

    def post(self, request):
        try:
            payload = ConstructionCostPredictionSerializer(data=request.data)
            if payload.is_valid():
                # load construction prediction model from predition_models folder
                # Get the absolute path to the current working directory
                absolute_path = "core/prediction_models/construction_cost_h5_model.h5"
                model = models.load_model(absolute_path)

                # load the preprocessor from the predition_models folder
                preprocessor_path = 'core/prediction_models/preprocessor.pkl'
                preprocessor = joblib.load(preprocessor_path)

                # Define preprocessing steps to match training phase
                categorical_features = ['building_function']
                numerical_features = ['building_height', 'builtup_area', 'number_of_stories', 'number_of_columns',
                                      'number_of_rooms', 'number_of_units']

                data = payload.validated_data
                logger.info(f"Construction Cost: data -> {data}")

                # Convert data to DataFrame
                df = DataFrame(data, index=[0])
                df.columns = ['building height', 'builtup area', 'number of stories', 'number of columns',
                              'number of rooms', 'building function', 'number of units']

                # Preprocess the input data
                X_preprocessed = preprocessor.transform(df)
                logger.info(f"Construction Cost: X_preprocessed -> {X_preprocessed}")

                # Make prediction
                prediction = model.predict(X_preprocessed)
                logger.info(f"Construction Cost: prediction -> {prediction}")

                # Inverse transform the prediction if necessary (assuming log transformation was used)
                prediction_exp = np.expm1(prediction)
                logger.info(f"Construction Cost: prediction_exp -> {prediction_exp}")

                return JsonResponse({'predicted_cost': float(prediction_exp[0][0])})
            else:
                return JsonResponse({"error": payload.errors}, status=400)
        except Exception as e:
            logger.error(f"Server Error: {str(e.with_traceback())}")
            return JsonResponse({"error": str(e)}, status=500)


class MaterialCostPredictionAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = MaterialCostPredictionSerializer

    def post(self, request):
        try:
            return JsonResponse({"message": "Hello World!"})
        except Exception as e:
            logger.error(f"Server Error: {str(e.with_traceback())}")
            return JsonResponse({"error": str(e)}, status=500)

