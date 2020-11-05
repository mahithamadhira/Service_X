from django.shortcuts import render, redirect
from django.contrib import sessions
import boto3
from boto3.dynamodb.conditions import Key, Attr
from django.contrib import sessions
from django.contrib import messages

# Create your views here.

def mech_dashboard(request):
	if request.session['is_staff'] =='true' :
		return render(request, 'dashboard/mech.html')
	return redirect('user_dashboard')
	return render(request,'dashboard/mech.html')

def user_dashboard(request):
	if request.method == 'POST':
		fname = request.POST.get('fname')
		lname = request.POST.get('lname')
		email_id = request.session['email_id']
		username = request.POST.get('username')
		gender = request.POST.get('gender')
		age = request.POST.get('age')
		is_admin = request.POST.get('is_admin')
		is_staff = request.POST.get('is_staff')
		contact = request.POST.get('contact')
		dLicense = request.POST.get('dLicense')
		dynamodb = boto3.resource('dynamodb')
		table = dynamodb.Table('User')
		response = table.update_item(
        Key={
            'email_id': email_id,
        },
        UpdateExpression="set fname=:fname, lname=:lname, username =:username, gender =:gender, age =:age, is_admin =:is_admin, is_staff =:is_staff, contact =:contact, dLicense = :dLicense",
        ExpressionAttributeValues={
            ':fname': fname,
            ':lname': lname,
            ':gender': gender,
			':username':username,
			':age':age,
			':is_admin':is_admin,
			':is_staff':is_staff,
			':contact' :contact,
			':dLicense' : dLicense, 
        },
        ReturnValues="UPDATED_NEW"
    	)
		dic = {}
		dynamodb = boto3.resource('dynamodb')
		table = dynamodb.Table('User')
		response = table.scan(
			FilterExpression=Attr('email_id').eq(email_id)
		)
		dic['email_id'] = response['Items'][0]['email_id']
		dic['fname'] = response['Items'][0]['fname']
		dic['lname'] = response['Items'][0]['lname']
		dic['username'] = response['Items'][0]['username']
		dic['age'] = response['Items'][0]['age']
		dic['gender'] = response['Items'][0]['gender']
		dic['dLicense'] =  response['Items'][0]['dLicense']
		dic['is_staff'] =  response['Items'][0]['is_staff']
		dic['is_admin'] =  response['Items'][0]['is_admin']
		dic['is_verified'] =  response['Items'][0]['is_verified']
		dic['contact'] =  response['Items'][0]['contact']
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
		return render(request,'dashboard/user.html',dic)
	else:
		email= request.session['email_id']
		dynamodb = boto3.resource('dynamodb')
		table = dynamodb.Table('User')
		response = table.scan(
			FilterExpression=Attr('email_id').eq(email)
		)
		dic = {}
		dic['email_id'] = email
		dic['fname'] = response['Items'][0]['fname']
		dic['lname'] = response['Items'][0]['lname']
		dic['username'] = response['Items'][0]['username']
		dic['age'] = response['Items'][0]['age']
		dic['gender'] = response['Items'][0]['gender']
		dic['dLicense'] =  response['Items'][0]['dLicense']
		dic['is_staff'] =  response['Items'][0]['is_staff']
		dic['is_admin'] =  response['Items'][0]['is_admin']
		dic['is_verified'] =  response['Items'][0]['is_verified']
		dic['contact'] =  response['Items'][0]['contact']
		return render(request,'dashboard/user.html',dic)

def employee_dashboard(request):
	if request.session['is_admin'] =='true' :
		return render(request, 'dashboard/emp.html')
	return redirect('user_dashboard')

def employee_earnings(request):
	if request.session['is_admin'] =='true' :
		return render(request, 'dashboard/emp_earn.html')
	return redirect('user_dashboard')

def mech_earnings(request):
	if request.session['is_staff'] =='true' :
		return render(request, 'dashboard/mech_earn.html')
	return redirect('user_dashboard')

def user_transactions(request):
	return render(request,'dashboard/user_earn.html')
