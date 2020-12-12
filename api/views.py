from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import viewsets, status
import boto3
from boto3.dynamodb.conditions import Key, Attr
dynamodb = boto3.resource('dynamodb')
car_table = dynamodb.Table('Car')
user_table = dynamodb.Table('User')
emp_table = dynamodb.Table('Employee')
cB_table = dynamodb.Table('bookings')
mB_table = dynamodb.Table('mBooking')
ver_table = dynamodb.Table('verifications')
mechanic_table = dynamodb.Table('Mechanic')

from . import serializers
from .serializers import Car, CarSerializer, MechanicSerializer, Mechanic, UserSerializer, User, EmployeeSerializer
from .serializers import Employee, Verify, VerifySerializer, cBooking, cBookingSerializer, mBooking, mBookingSerializer


# ------------------------------------------------------- CAR Crud ---------------------------------------------------------------#

class carGP(APIView):

    def get(self, request):
        carobj = car_table.scan()['Items']
        carsobj = CarSerializer(carobj,many=True)
        return Response(carsobj.data)

    def post(self,request):
        serializer = serializers.CarSerializer(data=request.data)
        if serializer.is_valid():
            task = serializer.save()
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

class carGDU(APIView):

    def get_object(self,pk):
        try:
            return car_table.scan(FilterExpression=Attr('email_id').eq(pk))['Items']
        except :
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def get(self,request,pk):
        carobj = self.get_object(pk)
        serobj = CarSerializer(carobj, many=True)
        return Response(serobj.data)
    
    def put(self,request):
        serializer = serializers.CarSerializer(data=request.data)
        if serializer.is_valid():
            task = serializer.save()
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

    def delete(self,request,pk):
        car_table.delete_item(key={'email_id':pk},)
        return Response(status=status.HTTP_204_NO_CONTENT)

# ------------------------------------------------------- Mechanic CRUD---------------------------------------------------------------#

class mechGP(APIView):

    def get(self, request):
        obj = mechanic_table.scan()['Items']
        serializer = MechanicSerializer(obj,many=True)
        return Response(serializer.data)

    def post(self,request):
        serializer = serializers.MechanicSerializer(data=request.data)
        if serializer.is_valid():
            task = serializer.save()
            mechanic_table.put_item(
                Item={
                    'email_id': task.email_id,
                    'g_name' : task.g_name,
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

class mechGDU(APIView):

    def get_object(self,pk):
        try:
            return mechanic_table.scan(FilterExpression=Attr('email_id').eq(pk))['Items']
        except :
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def get(self,request,pk):
        obj = self.get_object(pk)
        serializer = MechanicSerializer(obj,many=True)
        return Response(serializer.data)
    
    def post(self,request):
        serializer = serializers.MechanicSerializer(data=request.data)
        if serializer.is_valid():
            task = serializer.save()
            mechanic_table.put_item(
                Item={
                    'email_id': task.email_id,
                    'g_name' : task.g_name,
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
    
    def delete(self,request,pk):
        mechanic_table.delete_item(key={'email_id':pk},)
        return Response(status=status.HTTP_204_NO_CONTENT)

# ----------------------------------------------------USER CRUD---------------------------------------------------------------- #

class userGP(APIView):

    def get(self, request):
        obj = user_table.scan()['Items']
        serializer = UserSerializer(obj,many=True)
        return Response(serializer.data)

    def post(self,request):
        serializer = serializers.UserSerializer(data=request.data)
        if serializer.is_valid():
            task = serializer.save()
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

class userGDU(APIView):

    def get_object(self,pk):
        try:
            return user_table.scan(FilterExpression=Attr('email_id').eq(pk))['Items']
        except :
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def get(self,request,pk):
        obj = self.get_object(pk)
        serializer = UserSerializer(obj,many=True)
        return Response(serializer.data)
    
    def put(self,request,pk):
        serializer = serializers.UserSerializer(data=request.data)
        if serializer.is_valid():
            task = serializer.save()
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

    
    def delete(self,request,pk):
        user_table.delete_item(key={'email_id':pk},)
        return Response(status=status.HTTP_204_NO_CONTENT)

# ----------------------------------------------------Employee CRUD---------------------------------------------------------------- #

class employeeGP(APIView):

    def get(self, request):
        obj = emp_table.scan()['Items']
        serializer = EmployeeSerializer(obj,many=True)
        return Response(serializer.data)

    def post(self,request):
        serializer = serializers.EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            task = serializer.save()
            emp_table.put_item(
                Item={
                    'email_id': task.email_id,
                    'contact': task.contact,
                    'earnings': task.earnings,
                    'verified_count' : task.verified_count
                }
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class employeeGDU(APIView):

    def get_object(self,pk):
        try:
            return emp_table.scan(FilterExpression=Attr('email_id').eq(pk))['Items']
        except :
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def get(self,request,pk):
        obj = self.get_object(pk)
        serializer = EmployeeSerializer(obj,many=True)
        return Response(serializer.data)
    
    def put(self,request):
        serializer = serializers.EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            task = serializer.save()
            emp_table.put_item(
                Item={
                    'email_id': task.email_id,
                    'contact': task.contact,
                    'earnings': task.earnings,
                    'verified_count' : task.verified_count
                }
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,pk):
        emp_table.delete_item(key={'email_id':pk},)
        return Response(status=status.HTTP_204_NO_CONTENT)

# ----------------------------------------------------cBooking CRUD---------------------------------------------------------------- #

class cBookingGP(APIView):

    def get(self, request):
        obj = cB_table.scan()['Items']
        serializer = cBookingSerializer(obj,many=True)
        return Response(serializer.data)

    def post(self,request):
        serializer = serializers.cBookingSerializer(data=request.data)
        if serializer.is_valid():
            task = serializer.save()
            cB_table.put_item(
                Item={
                    'sr' : task.sr,
                    'buyer_email': task.buyer_email,
                    'car_name': task.car_name,
                    'car_number': task.car_number,
                    'owner_email' : task.owner_email,
                    'status' : task.status
                }
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class cBookingGDU(APIView):

    def get_object(self,pk):
        try:
            return cB_table.scan(FilterExpression=Attr('buyer_email').eq(pk))['Items']
        except :
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def get(self,request,pk):
        obj = self.get_object(pk)
        serializer = cBookingSerializer(obj,many=True)
        return Response(serializer.data)
    
    def put(self,request):
        serializer = serializers.cBookingSerializer(data=request.data)
        if serializer.is_valid():
            task = serializer.save()
            cB_table.put_item(
                Item={
                    'sr' : task.sr,
                    'buyer_email': task.buyer_email,
                    'car_name': task.car_name,
                    'car_number': task.car_number,
                    'owner_email' : task.owner_email,
                    'status' : task.status
                }
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ----------------------------------------------------mBooking CRUD---------------------------------------------------------------- #

class mBookingGP(APIView):

    def get(self, request):
        obj = mB_table.scan()['Items']
        serializer = mBookingSerializer(obj,many=True)
        return Response(serializer.data)

    def post(self,request):
        serializer = serializers.mBookingSerializer(data=request.data)
        if serializer.is_valid():
            task = serializer.save()
            mB_table.put_item(
                Item={
                    'sr' : str(task.sr),
                    'buyer_email': task.buyer_email,
                    'mech_email' : task.mech_email,
                    'status' : task.status
                }
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class mBookingGDU(APIView):

    def get_object(self,pk):
        try:
            return mB_table.scan(FilterExpression=Attr('buyer_email').eq(pk))['Items']
        except :
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def get(self,request,pk):
        obj = self.get_object(pk)
        serializer = mBookingSerializer(obj,many=True)
        return Response(serializer.data)
    
    def put(self,request):
        serializer = serializers.mBookingSerializer(data=request.data)
        if serializer.is_valid():
            task = serializer.save()
            mB_table.put_item(
                Item={
                    'sr' : str(task.sr),
                    'buyer_email': task.buyer_email,
                    'mech_email' : task.mech_email,
                    'status' : task.status
                }
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ----------------------------------------------------verifying CRUD---------------------------------------------------------------- #

class verGP(APIView):

    def get(self, request):
        obj = ver_table.scan()['Items']
        serializer = VerifySerializer(obj,many=True)
        return Response(serializer.data)

    def post(self,request):
        serializer = serializers.VerifySerializer(data=request.data)
        if serializer.is_valid():
            task = serializer.save()
            ver_table.put_item(
                Item={
                    'sr' : task.sr,
                    'checked_email': task.checked_email,
                    'employee_email' : task.employee_email,
                    'type_of' : task.type_of
                }
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class verGDU(APIView):

    def get_object(self,pk):
        try:
            return ver_table.scan(FilterExpression=Attr('checked_email').eq(pk))['Items']
        except :
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def get(self,request,pk):
        obj = self.get_object(pk)
        serializer = VerifySerializer(obj,many=True)
        return Response(serializer.data)

    def put(self,request):
        serializer = serializers.VerifySerializer(data=request.data)
        if serializer.is_valid():
            task = serializer.save()
            ver_table.put_item(
                Item={
                    'sr' : task.sr,
                    'checked_email': task.checked_email,
                    'employee_email' : task.employee_email,
                    'type_of' : task.type_of
                }
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,pk):
        ver_table.delete_item(key={'sr':pk},)
        return Response(status=status.HTTP_204_NO_CONTENT)

# ------------------------------------------------------------------------------------------------------------------------#


# -------------------------------------------------------- Car --------------------------------------------------------#
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
            task = car_table.scan(FilterExpression=Attr('email_id').eq(pk))['Items']
        except KeyError:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except ValueError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = serializers.CarSerializer(instance=task)
        return Response(serializer.data)

    def update(self, request, pk=None):
        try:
            for i in taskc:
                if i['email_id'] == str(pk):
                    task = i
                    break
        except KeyError:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except ValueError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = serializers.CarSerializer(
            data=request.data, instance=task)
        if serializer.is_valid():
            task = serializer.save()
            car_table.update_item(
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
            for i in taskc:
                if i['email_id'] == str(pk):
                    task = i
                    break
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
            car_table.update_item(
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
            for i in taskc:
                if i['email_id'] == str(pk):
                    task = i
                    break
        except KeyError:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except ValueError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        response = car_table.delete_item(
            Key={
                'email_id': pk
            }
        ) 
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
            for i in taskm:
                if i['email_id'] == str(pk):
                    task = i
                    break
        except KeyError:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except ValueError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = serializers.MechanicSerializer(instance=task)
        return Response(serializer.data)

    def update(self, request, pk=None):
        try:
            for i in taskm:
                if i['email_id'] == str(pk):
                    task = i
                    break
        except KeyError:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except ValueError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = serializers.MechanicSerializer(
            data=request.data, instance=task)
        if serializer.is_valid():
            task = serializer.save()
            # taskc.append(task)
            mechanic_table.update_item(
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
            for i in taskm:
                if i['email_id'] == str(pk):
                    task = i
                    break
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
            mechanic_table.update_item(
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
            for i in taskm:
                if i['email_id'] == str(pk):
                    task = i
                    break
        except KeyError:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except ValueError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        response = mechanic_table.delete_item(
            Key={
                'email_id': pk
            }
        )
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
            for i in tasku:
                if i['email_id'] == str(pk):
                    task = i
                    break
        except KeyError:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except ValueError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = serializers.UserSerializer(instance=task)
        return Response(serializer.data)

    def update(self, request, pk=None):
        try:
            for i in tasku:
                if i['email_id'] == str(pk):
                    task = i
                    break
        except KeyError:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except ValueError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = serializers.UserSerializer(
            data=request.data, instance=task)
        if serializer.is_valid():
            task = serializer.save()
            # taskc.append(task)
            user_table.update_item(
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
            for i in tasku:
                if i['email_id'] == str(pk):
                    task = i
                    break
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
            user_table.update_item(
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
            for i in tasku:
                if i['email_id'] == str(pk):
                    task = i
                    break
        except KeyError:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except ValueError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        response = user_table.delete_item(
            Key={
                'email_id': pk
            }
        )
        return Response(status=status.HTTP_204_NO_CONTENT)

# ------------------------------------------------------------------------------------------------------------------------------------------------------ #
