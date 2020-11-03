from django.shortcuts import render,redirect
import boto3
from boto3.dynamodb.conditions import Key, Attr
from django.http import HttpResponse
from django.core.mail import send_mail
from django.shortcuts import render,redirect
#from rest_framework.response import Response
# from rest_framework.views import APIView
# from rest_framework import status
# from django.contrib import sessions
from django.contrib import messages
# from django.contrib.sites.shortcuts import get_current_site
# from django.utils.encoding import force_bytes, force_text
# from django.template.loader import render_to_string
#from .tokens import account_activation_token
# from django.contrib.auth.decorators import login_required
# from django.contrib.auth import logout
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
        age = request.POST.get('age')
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
                    }
                )
                return redirect('home')
            else:
                messages.success(request, 'The email ID is already registerd')
        else:
            messages.success(request, 'Failed to register as the password and confirm password do not match')
    return render(request,'register/signup.html')

def login(request):
    if request.method == 'POST':
        email_id = request.POST.get('email')
        password = request.POST.get('password')
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('User')
        response = table.scan(FilterExpression=Attr('email_id').eq(email_id))
        if(len(response['Items'])>0):
            if(response['Items'][0]['password']==password):
                return redirect('home')
            else:
                messages.success(request, 'Failed to login as the password does not match.')
                return redirect('login')
        else:
            messages.success(request, 'Failed to login as the email ID is not registered.')
            return redirect('signup')
    return render(request,'register/login.html')

