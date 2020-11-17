from rest_framework import serializers

# ---------------------------------------------------------------- CAR ------------------------------------------------------#
class Car(object):
    def __init__(self, **kwargs):
        for field in ('email_id', 'car_name', 'car_number', 'car_model','co_ordinates', 'cost_perday', 'earnings','rating','is_available','is_verified'):
            setattr(self, field, kwargs.get(field, None))

class CarSerializer(serializers.Serializer):
    email_id            = serializers.CharField(max_length=30)
    car_number          = serializers.CharField(max_length=30)
    car_model           = serializers.CharField(max_length=30)
    car_name            = serializers.CharField(max_length=30)
    co_ordinates        = serializers.CharField(max_length=30)
    cost_perday         = serializers.IntegerField()
    earnings            = serializers.IntegerField()
    rating              = serializers.IntegerField()
    is_available        = serializers.BooleanField()
    is_verified         = serializers.BooleanField()

    def create(self, validated_data):
        return Car(**validated_data)

    def update(self, instance, validated_data):
        for field, value in validated_data.items():
            setattr(instance, field, value)
        return instance


# ------------------------------------------------------------- Mechanical ---------------------------------------------------#

class Mechanic(object):
    def __init__(self, **kwargs):
        for field in ('email_id', 'co_ordinates', 'earnings','rating','service_charge','is_available','is_verified'):
            setattr(self, field, kwargs.get(field, None))

class MechanicSerializer(serializers.Serializer):
    email_id            = serializers.CharField(max_length=30)
    co_ordinates        = serializers.CharField(max_length=30)
    earnings            = serializers.IntegerField()
    rating              = serializers.IntegerField()
    service_charge      = serializers.IntegerField()
    is_available        = serializers.BooleanField()
    is_verified         = serializers.BooleanField()

    def create(self, validated_data):
        return Mechanic(**validated_data)

    def update(self, instance, validated_data):
        for field, value in validated_data.items():
            setattr(instance, field, value)
        return instance



# ------------------------------------------------------------- USER --------------------------------------------------------#
class User(object):
    def __init__(self, **kwargs):
        for field in ('email_id', 'fname', 'lname','username','age','gender','contact', 'dLicense'):
            setattr(self, field, kwargs.get(field, None))


class UserSerializer(serializers.Serializer):
    email_id            = serializers.CharField(max_length=30)
    fname               = serializers.CharField(max_length=30)
    lname               = serializers.CharField(max_length=30)
    username            = serializers.CharField(max_length=30)
    age                 = serializers.IntegerField()
    gender              = serializers.CharField(max_length=1)
    contact             = serializers.CharField(max_length=30)
    dLicense            = serializers.CharField(max_length=30)

    def create(self, validated_data):
        return User(**validated_data)

    def update(self, instance, validated_data):
        for field, value in validated_data.items():
            setattr(instance, field, value)
        return instance