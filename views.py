from rest_framework.response import Response
from rest_framework import viewsets, status
import boto3
from boto3.dynamodb.conditions import Key, Attr
dynamodb = boto3.resource('dynamodb')
car_table = dynamodb.Table('Car')
user_table = dynamodb.Table('User')
mechanic_table = dynamodb.Table('Mechanic')

from . import serializers
from .serializers import Car, CarSerializer, MechanicSerializer, Mechanic, UserSerializer, User

# -------------------------------------------------------- Car ----------------------------------------------------#
taskc = car_table.scan()['Items']
class CarViewSet(viewsets.ViewSet):
    serializer_class = serializers.CarSerializer

    def list(self, request):
        serializer = CarSerializer(instance=taskc, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = serializers.CarSerializer(data=request.data)
        if serializer.is_valid():
            task = serializer.save()
            taskc.append(task)
            print(task.email_id)
            car_table.put_item(
                Item={
                    'email_id': task.email_id,
                    'car_name': task.car_name,
                    'car_model': task.car_model,
                    'car_number': task.car_number,
                    'co_ordinates': task.co_ordinates,
                    'cost_perday': task.cost_perday,
                    'earnings': task.earnings,
                    'rating': task.rating,
                    'is_available': task.is_available,
                    'is_verified': task.is_verified,
                }
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        try:
            task = taskc[str(pk)]
        except KeyError:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except ValueError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = serializers.CarSerializer(instance=task)
        return Response(serializer.data)

    def update(self, request, pk=None):
        try:
            task = taskc[str(pk)]
        except KeyError:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except ValueError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = serializers.CarSerializer(
            data=request.data, instance=task)
        if serializer.is_valid():
            task = serializer.save()
            # taskc.append(task)
            car_table.put_item(
                Item={
                    'email_id': task.email_id,
                    'car_name': task.car_name,
                    'car_model': task.car_model,
                    'car_number': task.car_number,
                    'co_ordinates': task.co_ordinates,
                    'cost_perday': task.cost_perday,
                    'earnings': task.earnings,
                    'rating': task.rating,
                    'is_available': task.is_available,
                    'is_verified': task.is_verified,
                }
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        try:
            task = taskc[str(pk)]
        except KeyError:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except ValueError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = serializers.CarSerializer(
            data=request.data,
            instance=task,
            partial=True)
        if serializer.is_valid():
            task = serializer.save()
            # taskc.append(task)
            car_table.put_item(
                Item={
                    'email_id': task.email_id,
                    'car_name': task.car_name,
                    'car_model': task.car_model,
                    'car_number': task.car_number,
                    'co_ordinates': task.co_ordinates,
                    'cost_perday': task.cost_perday,
                    'earnings': task.earnings,
                    'rating': task.rating,
                    'is_available': task.is_available,
                    'is_verified': task.is_verified,
                }
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        try:
            task = taskc[str(pk)]
        except KeyError:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except ValueError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        del taskc[task.email_id]
        return Response(status=status.HTTP_204_NO_CONTENT)


# ----------------------------------------------------------------------- Mechanic ---------------------------------------------------------------#

taskm = mechanic_table.scan()['Items']
class MechanicViewSet(viewsets.ViewSet):
    serializer_class = serializers.MechanicSerializer

    def list(self, request):
        serializer = MechanicSerializer(instance=taskm, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = serializers.MechanicSerializer(data=request.data)
        if serializer.is_valid():
            task = serializer.save()
            # taskc.append(task)
            mechanic_table.put_item(
                Item={
                    'email_id': task.email_id,
                    'co_ordinates': task.co_ordinates,
                    'earnings': task.earnings,
                    'rating': task.rating,
                    'service_charge' : task.service_charge,
                    'is_available': task.is_available,
                    'is_verified': task.is_verified,
                }
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        try:
            task = taskm[str(pk)]
        except KeyError:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except ValueError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = serializers.MechanicSerializer(instance=task)
        return Response(serializer.data)

    def update(self, request, pk=None):
        try:
            task = taskm[str(pk)]
        except KeyError:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except ValueError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = serializers.MechanicSerializer(
            data=request.data, instance=task)
        if serializer.is_valid():
            task = serializer.save()
            # taskc.append(task)
            mechanic_table.put_item(
                Item={
                    'email_id': task.email_id,
                    'co_ordinates': task.co_ordinates,
                    'earnings': task.earnings,
                    'rating': task.rating,
                    'service_charge' : task.service_charge,
                    'is_available': task.is_available,
                    'is_verified': task.is_verified,
                }
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        try:
            task = taskm[str(pk)]
        except KeyError:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except ValueError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = serializers.MechanicSerializer(
            data=request.data,
            instance=task,
            partial=True)
        if serializer.is_valid():
            task = serializer.save()
            # taskc.append(task)
            mechanic_table.put_item(
                Item={
                    'email_id': task.email_id,
                    'co_ordinates': task.co_ordinates,
                    'earnings': task.earnings,
                    'rating': task.rating,
                    'service_charge' : task.service_charge,
                    'is_available': task.is_available,
                    'is_verified': task.is_verified,
                }
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        try:
            task = taskm[str(pk)]
        except KeyError:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except ValueError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        del taskm[task.email_id]
        return Response(status=status.HTTP_204_NO_CONTENT)

# ------------------------------------------------------------------- USER -----------------------------------------------------------#

tasku = user_table.scan()['Items']
class UserViewSet(viewsets.ViewSet):
    serializer_class = serializers.UserSerializer

    def list(self, request):
        serializer = UserSerializer(instance=tasku, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = serializers.UserSerializer(data=request.data)
        if serializer.is_valid():
            task = serializer.save()
            # taskc.append(task)
            user_table.put_item(
                Item={
                    'email_id': task.email_id,
                    'fname': task.fname,
                    'lname': task.lname,
                    'username': task.username,
                    'age' : task.age,
                    'gender': task.gender,
                    'contact': task.contact,
                    'dLicense' : task.dLicense,
                }
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        try:
            task = tasku[str(pk)]
        except KeyError:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except ValueError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = serializers.UserSerializer(instance=task)
        return Response(serializer.data)

    def update(self, request, pk=None):
        try:
            task = tasku[str(pk)]
        except KeyError:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except ValueError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = serializers.UserSerializer(
            data=request.data, instance=task)
        if serializer.is_valid():
            task = serializer.save()
            # taskc.append(task)
            user_table.put_item(
                Item={
                    'email_id': task.email_id,
                    'fname': task.fname,
                    'lname': task.lname,
                    'username': task.username,
                    'age' : task.age,
                    'gender': task.gender,
                    'contact': task.contact,
                    'dLicense' : task.dLicense,
                }
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        try:
            task = tasku[str(pk)]
        except KeyError:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except ValueError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = serializers.UserSerializer(
            data=request.data,
            instance=task,
            partial=True)
        if serializer.is_valid():
            task = serializer.save()
            # taskc.append(task)
            user_table.put_item(
                Item={
                    'email_id': task.email_id,
                    'fname': task.fname,
                    'lname': task.lname,
                    'username': task.username,
                    'age' : task.age,
                    'gender': task.gender,
                    'contact': task.contact,
                    'dLicense' : task.dLicense,
                }
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        try:
            task = tasku[str(pk)]
        except KeyError:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except ValueError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        del tasku[task.email_id]
        return Response(status=status.HTTP_204_NO_CONTENT)

# ------------------------------------------------------------------------------------------------------------------------------------------------------ #