from rest_framework import serializers


class ConstructionCostPredictionSerializer(serializers.Serializer):
    """
    building height
    builtup area
    number of stories
    number of columns
    number of rooms
    building function
    number of units
    total project cost
    """
    building_height = serializers.FloatField(required=True)
    builtup_area = serializers.FloatField(required=True)
    number_of_stories = serializers.IntegerField(required=True)
    number_of_columns = serializers.IntegerField(required=True)
    number_of_rooms = serializers.IntegerField(required=True)
    building_function = serializers.CharField(required=True)
    number_of_units = serializers.IntegerField(required=True)


class MaterialCostPredictionSerializer(serializers.Serializer):
    """
    inflationrate	imports	exports	moneysupplym1	BMI
    """
    inflation_rate = serializers.FloatField(required=True)
    imports = serializers.FloatField(required=True)
    exports = serializers.FloatField(required=True)
    money_supply_m1 = serializers.FloatField(required=True)

