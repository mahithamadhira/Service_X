from django.shortcuts import render,redirect
import boto3
from boto3.dynamodb.conditions import Key, Attr
from django.http import HttpResponse
from django.core.mail import send_mail
from django.shortcuts import render,redirect
#from rest_framework.response import Response
# from rest_framework.views import APIView
# from rest_framework import status
from django.contrib import sessions
from django.contrib import messages
# from django.contrib.sites.shortcuts import get_current_site
# from django.utils.encoding import force_bytes, force_text
# from django.template.loader import render_to_string
#from .tokens import account_activation_token
# from django.contrib.auth.decorators import login_required
# from django.contrib.auth import logout
from decimal import *
from django.core.files.storage import FileSystemStorage

# Create your views here.
def signup(request):
    if request.method == 'POST':
        print('request')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        username = request.POST.get('username')
        email_id = request.POST.get('email')
        password = request.POST.get('password')
        re_password = request.POST.get('re_password')
        gender = request.POST.get('gender')
        age = int(request.POST.get('age'))
        print(age)
        if(password==re_password):
            print('a')
            dynamodb = boto3.resource('dynamodb')
            table = dynamodb.Table('User')
            response = table.scan(
                ProjectionExpression="email_id",
                FilterExpression=Attr('email_id').eq(email_id)
            )
            print('b')
            if(len(response['Items'])==0):
                print('c')
                response = table.put_item(
                Item={
                    'fname': fname,
                    'email_id': email_id,
                    'password': password,
                    'lname': lname,
                    'username': username,
                    'age': age,
                    'gender': gender,
                    'contact': '-',
                    'dLicense':'-',
                    'is_admin':False,
                    'is_staff':False,
                    'is_verified':False,
                    }
                )
                response = table.scan(
                    FilterExpression=Attr('email_id').eq(email_id)
                )
                request.session['email_id']=response['Items'][0]['email_id']
                request.session['password']=response['Items'][0]['password']
                request.session['fname']=response['Items'][0]['fname']
                request.session['lname']=response['Items'][0]['lname']
                request.session['username']=response['Items'][0]['username']
                request.session['age']=int(response['Items'][0]['age'])
                request.session['gender']=response['Items'][0]['gender']
                request.session['is_admin'] = response['Items'][0]['is_admin']
                request.session['is_staff'] = response['Items'][0]['is_staff']
                request.session['is_verified'] = response['Items'][0]['is_verified']
                request.session['contact'] = response['Items'][0]['contact']
                request.session['dLicense'] = response['Items'][0]['dLicense']

                dynamodb = boto3.resource('dynamodb')
                table = dynamodb.Table('Car')
                response = table.put_item(
                    Item = {
                        'email_id':email_id,
                        'car_model':'0',
                        'car_name':'none',
                        'car_number':'none',
                        'co_ordinates':'-',
                        'cost_perday':0,
                        'earnings' :0,
                        'is_available':False,
                        'is_verified' : False,
                        'rating' : -1,
                    }
                )
                response = table.scan(
                    FilterExpression=Attr('email_id').eq(email_id)
                )
                print(response['Items'])

                #request.session['email_id'] = response['Items'][0]['email_id']
                request.session['car_model'] = response['Items'][0]['car_model']
                request.session['car_name'] = response['Items'][0]['car_name']
                request.session['car_number'] = response['Items'][0]['car_number']
                request.session['co_ordinates'] = response['Items'][0]['co_ordinates']
                request.session['cost_perday'] = int(response['Items'][0]['cost_perday'])
                request.session['earnings'] = int(response['Items'][0]['earnings'])
                request.session['is_available'] = response['Items'][0]['is_available']
                request.session['is_verified'] = response['Items'][0]['is_verified']
                request.session['rating'] = int(response['Items'][0]['rating'])
                print('ikkada unna')
                print(type(request.session['is_verified']))
                print(request.session['is_verified'])
                print(type(request.session['rating']))
                return redirect('user_dashboard')
            else:
                messages.success(request, 'The email ID is already registerd')
        else:
            messages.success(request, 'Failed to register as the password and confirm password do not match')
    return render(request,'register/signup.html')

def login(request):
    if request.method == 'POST':
        email_id = request.POST.get('email')
        print(email_id)
        password = request.POST.get('password')
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('User')
        response = table.scan(FilterExpression=Attr('email_id').eq(email_id))
        print(response)
        if(len(response['Items'])>0):
            print(response)
            if(response['Items'][0]['password']==password):
                request.session['email_id']=response['Items'][0]['email_id']
                request.session['password']=response['Items'][0]['password']
                request.session['fname']=response['Items'][0]['fname']
                request.session['lname']=response['Items'][0]['lname']
                request.session['username']=response['Items'][0]['username']
                request.session['age']=response['Items'][0]['age']
                request.session['gender']=response['Items'][0]['gender']
                request.session['is_admin'] = response['Items'][0]['is_admin']
                request.session['is_staff'] = response['Items'][0]['is_staff']
                request.session['is_verified'] = response['Items'][0]['is_verified']
                request.session['contact'] = response['Items'][0]['contact']
                request.session['dLicense'] = response['Items'][0]['dLicense']
                #print(request.session['email_id'])
                return redirect('home')
            else:
                messages.success(request, 'Failed to login as the password does not match.')
                return redirect('login')
        else:
            messages.success(request, 'Failed to login as the email ID is not registered.')
            return redirect('signup')
    return render(request,'register/login.html')


def logout(request):
    try:
        request.session.flush()
        return redirect('home')
    except:
        return redirect('home')
