from django.shortcuts import render, redirect
from django.contrib import sessions
import boto3
from boto3.dynamodb.conditions import Key, Attr
from django.contrib import sessions
from django.contrib import messages

# Create your views here.

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

		if is_staff == 'true' and is_admin == 'true':
			messages.success(request, "You can't be both employee and mechanic.")
			return redirect('user_dashboard')
		else:
			if(is_staff == 'true'):
				is_staff = True
			else:
				is_staff = False

			if(is_admin == 'true'):
				is_admin = True
			else:
				is_admin = False
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
			dic['age'] = int(response['Items'][0]['age'])
			dic['gender'] = response['Items'][0]['gender']
			dic['dLicense'] =  response['Items'][0]['dLicense']
			dic['is_staff'] =  response['Items'][0]['is_staff']
			dic['is_admin'] =  response['Items'][0]['is_admin']
			dic['is_verified'] =  response['Items'][0]['is_verified']
			dic['contact'] =  response['Items'][0]['contact']
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

			if is_staff == True:
				dynamodb = boto3.resource('dynamodb')
				table = dynamodb.Table('Mechanic')
				response = table.scan(
                ProjectionExpression="email_id",
                FilterExpression=Attr('email_id').eq(email_id)
            	)
				if(len(response['Items'])==0):
					response = table.put_item(
						Item = {
							'email_id':email_id,
							'co_ordinates':'-',
							'service_charge':0,
							'earnings' :0,
							'is_available':False,
							'is_verified' : False,
							'rating' : 0,
						}
					)
					response = table.scan(
						FilterExpression=Attr('email_id').eq(email_id)
					)
					print(response['Items'])

					#request.session['email_id'] = response['Items'][0]['email_id']
					request.session['co_ordinates_mech'] = response['Items'][0]['co_ordinates']
					request.session['service_charge_mech'] =int(response['Items'][0]['service_charge'])
					request.session['earnings_mech'] = int(response['Items'][0]['earnings'])
					request.session['is_available_mech'] = response['Items'][0]['is_available']
					request.session['is_verified_mech'] = response['Items'][0]['is_verified']
					request.session['rating_mech'] = int(response['Items'][0]['rating'])
			if is_admin == True:
				dynamodb = boto3.resource('dynamodb')
				table = dynamodb.Table('Employee')
				response = table.scan(
					ProjectionExpression="email_id",
					FilterExpression=Attr('email_id').eq(email_id)
				)
				print(response)
				if(len(response['Items'])==0):
					response = table.put_item(
						Item = {
							'email_id':request.session['email_id'],
							'contact':request.session['contact'],
							'verified_count':0,
							'earnings' : 0,
						}
					)
					response = table.scan(
						FilterExpression=Attr('email_id').eq(email_id)
					)
					print(response['Items'])
					request.session['verified_count_emp'] = int(response['Items'][0]['verified_count'])
					request.session['earnings_emp'] = int(response['Items'][0]['earnings'])
			if is_admin == False:
				dynamodb = boto3.resource('dynamodb')
				table = dynamodb.Table('Employee')
				response = table.scan(
					FilterExpression=Attr('email_id').eq(email_id)
				)
				if(len(response['Items']) >0) :
					response = table.delete_item(
						Key = {
							'email_id':email_id,
						}
					)
			if is_staff == False:
				dynamodb = boto3.resource('dynamodb')
				table = dynamodb.Table('Mechanic')
				response = table.scan(
					FilterExpression=Attr('email_id').eq(email_id)
				)
				if(len(response['Items']) >0) :
					response = table.delete_item(
						Key = {
							'email_id':email_id,
						}
					)
			return render(request,'dashboard/user.html',dic)
	else:
		try:
			request.session['email_id']
		except:
			return redirect('login')
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
			dic['age'] = int(response['Items'][0]['age'])
			dic['gender'] = response['Items'][0]['gender']
			dic['dLicense'] =  response['Items'][0]['dLicense']
			dic['is_staff'] =  response['Items'][0]['is_staff']
			dic['is_admin'] =  response['Items'][0]['is_admin']
			dic['is_verified'] =  response['Items'][0]['is_verified']
			dic['contact'] =  response['Items'][0]['contact']

			email_id= request.session['email_id']
			dynamodb = boto3.resource('dynamodb')
			table = dynamodb.Table('Employee')
			response = table.scan(
				FilterExpression=Attr('email_id').eq(email_id)
			)
			if(len(response['Items'])>0):
				request.session['earnings_emp'] = int(response['Items'][0]['earnings'])
				request.session['verified_count_emp'] = int(response['Items'][0]['verified_count'])

			email_id= request.session['email_id']
			dynamodb = boto3.resource('dynamodb')
			table = dynamodb.Table('Mechanic')
			response = table.scan(
				FilterExpression=Attr('email_id').eq(email_id)
			)
			if(len(response['Items'])>0):
				request.session['co_ordinates_mech'] = response['Items'][0]['co_ordinates']
				request.session['service_charge_mech'] =int(response['Items'][0]['service_charge'])
				request.session['earnings_mech'] = int(response['Items'][0]['earnings'])
				request.session['is_available_mech'] = response['Items'][0]['is_available']
				request.session['is_verified_mech'] = response['Items'][0]['is_verified']
				request.session['rating_mech'] = int(response['Items'][0]['rating'])
			return render(request,'dashboard/user.html',dic)


def employee_earnings(request):
	if request.session['is_admin'] ==True :
		email= request.session['email_id']
		dynamodb = boto3.resource('dynamodb')
		table = dynamodb.Table('verifications')
		response = table.scan(
			FilterExpression=Attr('employee_email').eq(email)
		)
		dic = {}
		verified_cars= []
		verified_mechs = []
		for i in response['Items']:
			if(i['type_of'] == 'cars'):
				verified_cars.append(i)
			else:
				verified_mechs.append(i)
		dic['verified_cars'] = verified_cars
		dic['verified_mechs'] = verified_mechs		
		return render(request, 'dashboard/emp_earn.html',dic)
	return redirect('user_dashboard')

def mech_earnings(request):
	if request.session['is_staff'] ==True :
		return render(request, 'dashboard/mech_earn.html')
	return redirect('user_dashboard')

def user_took(request):
	return render(request,'dashboard/took_car.html')

def user_gib(request):
	if request.method == 'POST' :
		if(request.session['dLicense']=='-' or request.session['contact']=='-'):
			messages.success(request, "Please fill the contact number and/or license number")
			return redirect('user_gib')
		else:
			car_name = request.POST.get('car_name')
			car_number = request.POST.get('car_number')
			email_id = request.session['email_id']
			car_model = request.POST.get('car_model')
			# co_ordinates = request.POST.get('co_ordinates')
			cost_perday = int(request.POST.get('cost_perday'))
			is_available = request.POST.get('is_available')
			lat = request.POST.get('lat')
			long = request.POST.get('long')
			co_ordinates = '['
			co_ordinates+=lat
			co_ordinates+=','
			co_ordinates+=long
			co_ordinates+=']'
			print(co_ordinates)
			#is_verified = request.POST.get('is_verified')
			#rating = int(request.POST.get('rating'))
			#earnings = int(request.POST.get('earnings'))


			if(is_available == 'true'):
				is_available = True
			else:
				is_available = False

			# print("=========================================================================================")
			# print('Before updating')
			# print(type(cost_perday))
			# #print(type(rating))
			# #print(type(earnings))
			# print(type(is_available))
			# #print(type(is_verified))

			dynamodb = boto3.resource('dynamodb')
			table = dynamodb.Table('Car')
			response = table.update_item(
				Key={
					'email_id': email_id,
				},
				UpdateExpression="set car_name=:car_name, car_number=:car_number, car_model =:car_model, co_ordinates =:co_ordinates, cost_perday = :cost_perday, is_available =:is_available",
				ExpressionAttributeValues={
					':car_name': car_name,
					':car_number': car_number,
					':car_model': car_model,
					':co_ordinates':co_ordinates,
					':cost_perday':cost_perday,
					':is_available':is_available,
				},
				ReturnValues="UPDATED_NEW"
			)
			dic = {}
			dynamodb = boto3.resource('dynamodb')
			table = dynamodb.Table('Car')
			response = table.scan(
				FilterExpression=Attr('email_id').eq(email_id)
			)

			print('table scan')
			print(response['Items'][0]['co_ordinates'])
			print(type(response['Items'][0]['co_ordinates']))
			print(response['Items'][0]['co_ordinates'][0])
			lat = ""
			long = ""
			temp=0
			for i in response['Items'][0]['co_ordinates'][1:-1]:
				if i==',':
					temp=1
				elif temp==0:
					lat+=i
				else:
					long+=i

			dic['email_id'] = email_id
			dic['car_name'] = response['Items'][0]['car_name']
			dic['car_number'] = response['Items'][0]['car_number']
			dic['car_model'] = response['Items'][0]['car_model']
			dic['co_ordinates'] = response['Items'][0]['co_ordinates']

			dic['lat'] = float(lat)
			dic['long'] = float(long)

			print(dic['lat'])

			dic['cost_perday'] = response['Items'][0]['cost_perday']
			dic['is_available'] =  response['Items'][0]['is_available']
			dic['is_verified'] =  response['Items'][0]['is_verified']
			dic['rating'] =  response['Items'][0]['rating']
			dic['earnings'] =  response['Items'][0]['earnings']
			print('ayyindi mari')
			return render(request,'dashboard/gave_car.html',dic)
			# print("=========================================================================================")
			# print('After updating')
			# print(type(cost_perday))
			# #print(type(rating))
			# #print(type(earnings))
			# print(type(is_available))
			# #print(type(is_verified))
			# print("==========================================================================================")		
	else:
		email = request.session['email_id']
		dic = {}
		dynamodb = boto3.resource('dynamodb')
		table = dynamodb.Table('Car')
		response = table.scan(
			FilterExpression=Attr('email_id').eq(email)
		)
		print(response['Items'])
		dic['email_id'] = email
		if(response['Items'][0]['car_name'] == "none"):
			dic['car_name']=""
		else:
			dic['car_name'] = response['Items'][0]['car_name']

		if(response['Items'][0]['car_number'] == "none"):
			dic['car_number']=""
		else:
			dic['car_number'] = response['Items'][0]['car_number']

		if(response['Items'][0]['car_model'] == "none"):
			dic['car_model']=""
		else:
			dic['car_model'] = response['Items'][0]['car_model']
		dic['co_ordinates'] = response['Items'][0]['co_ordinates']

		lat = ""
		long = ""
		temp=0
		if response['Items'][0]['co_ordinates']!='-':
			for i in response['Items'][0]['co_ordinates'][1:-1]:
				if i==',':
					temp=1
				elif temp==0:
					lat+=i
				else:
					long+=i
		else:
			lat="17.18"
			long="87.14"
		print(lat)
		print(type(lat))
		dic['lat'] = float(lat)
		dic['long'] = float(long)

		print(dic['lat'])
		dic['cost_perday'] = response['Items'][0]['cost_perday']
		dic['is_available'] =  response['Items'][0]['is_available']
		dic['is_verified'] =  response['Items'][0]['is_verified']
		dic['rating'] =  response['Items'][0]['rating']
		dic['earnings'] =  response['Items'][0]['earnings']
		return render(request,'dashboard/gave_car.html',dic)

def mech_dashboard(request):
	if request.session['is_staff'] ==True :
		if request.method == 'POST':
			contact = request.session['contact']
			email_id = request.session['email_id']
			co_ordinates = request.POST.get('co_ordinates')
			service_charge = int(request.POST.get('service_charge'))
			#earnings = request.session['earnings']
			is_available = request.POST.get('is_available')
			#is_verified = request.session['is_verified']
			#rating = request.session['rating']
			lat = request.POST.get('lat')
			long = request.POST.get('long')
			co_ordinates = '['
			co_ordinates+=lat
			co_ordinates+=','
			co_ordinates+=long
			co_ordinates+=']'
			if(is_available == 'true'):
				is_available = 'True'
			else:
				is_available = 'False'

			dynamodb = boto3.resource('dynamodb')
			table = dynamodb.Table('Mechanic')
			response = table.update_item(
				Key={
					'email_id': email_id,
				},
				UpdateExpression="set co_ordinates=:co_ordinates, service_charge=:service_charge, is_available =:is_available",
				ExpressionAttributeValues={
					':co_ordinates': co_ordinates,
					':service_charge': service_charge,
					':is_available':is_available,
				},
				ReturnValues="UPDATED_NEW"
			)
			print('updated values')
			dic = {}
			dynamodb = boto3.resource('dynamodb')
			table = dynamodb.Table('Mechanic')
			response = table.scan(
				FilterExpression=Attr('email_id').eq(email_id)
			)
			print('scanning')
			lat = ""
			long = ""
			temp=0
			for i in response['Items'][0]['co_ordinates'][1:-1]:
				if i==',':
					temp=1
				elif temp==0:
					lat+=i
				else:
					long+=i
			print(lat)
			print(type(lat))
			dic['lat'] = float(lat)
			dic['long'] = float(long)

			print(dic['lat'])
			dic['email_id'] = response['Items'][0]['email_id']
			dic['contact'] = request.session['contact']
			dic['co_ordinates'] = response['Items'][0]['co_ordinates']
			dic['service_charge'] = response['Items'][0]['service_charge']
			dic['earnings'] = response['Items'][0]['earnings']
			dic['is_available'] = response['Items'][0]['is_available']
			dic['is_verified'] = response['Items'][0]['is_verified']
			dic['rating'] = response['Items'][0]['rating']
			print('umm')
			return render(request,'dashboard/mech.html',dic)
		else:
			email_id = request.session['email_id']
			dic = {}
			dynamodb = boto3.resource('dynamodb')
			table = dynamodb.Table('Mechanic')
			response = table.scan(
				FilterExpression=Attr('email_id').eq(email_id)
			)
			lat = ""
			long = ""
			temp=0
			if response['Items'][0]['co_ordinates']!='-':
				for i in response['Items'][0]['co_ordinates'][1:-1]:
					if i==',':
						temp=1
					elif temp==0:
						lat+=i
					else:
						long+=i
			else:
				lat="17.18"
				long="87.14"
			print(lat)
			print(type(lat))
			dic['lat'] = float(lat)
			dic['long'] = float(long)

			print(dic['lat'])
			dic['email_id'] = response['Items'][0]['email_id']
			dic['contact'] = request.session['contact']
			dic['co_ordinates'] = response['Items'][0]['co_ordinates']
			dic['service_charge'] = response['Items'][0]['service_charge']
			dic['earnings'] = response['Items'][0]['earnings']
			dic['is_available'] = response['Items'][0]['is_available']
			dic['is_verified'] = response['Items'][0]['is_verified']
			dic['rating'] = response['Items'][0]['rating']
			return render(request,'dashboard/mech.html',dic)
	else:
		return redirect('user_dashboard')

def employee_dashboard(request):
	if request.session['is_admin'] ==True :
		if request.method == 'POST':
			email = request.POST.get('email_id')
			typ = request.POST.get('type')
			is_verified = True
			if(typ == 'cars'):
				dynamodb = boto3.resource('dynamodb')
				table = dynamodb.Table('Car')
				response = table.update_item(
					Key={
						'email_id': email,
					},
					UpdateExpression="set is_verified =:is_verified",
					ExpressionAttributeValues={
						':is_verified':is_verified,
					},
					ReturnValues="UPDATED_NEW"
				)

				email_id = request.session['email_id']
				for key, value in request.session.items():
   					print('{} => {}'.format(key, value))
				earnings = request.session['earnings_emp']
				print('============kars===================')
				print(earnings)
				earnings = earnings + 1000
				print(earnings)

				verified_count = request.session['verified_count_emp']
				verified_count+=1

				table = dynamodb.Table('Employee')
				response = table.update_item(
					Key={
						'email_id': email_id,
					},
					UpdateExpression="set earnings =:earnings, verified_count = :verified_count",
					ExpressionAttributeValues={
						':earnings':earnings,
						':verified_count':verified_count,
					},
					ReturnValues="UPDATED_NEW"
				)
				request.session['earnings_emp'] = earnings
				request.session['verified_count_emp'] = verified_count


				table = dynamodb.Table('verifications')
				response = table.scan()
				sr = 0
				if(len(response['Items'])==0):
					sr = 1
				else:
					temp = 0
					for i in response['Items']:
						if temp<int(i['sr']):
							temp = int(i['sr'])
					sr = temp+1
				print(sr)
				response = table.put_item(
					Item = {
						'sr': sr,
						'employee_email':email_id,
						'checked_email':email,
						'type_of': typ,
					}
				)



			if(typ == 'mechanics'):
				dynamodb = boto3.resource('dynamodb')
				table = dynamodb.Table('Mechanic')
				response = table.update_item(
					Key={
						'email_id': email,
					},
					UpdateExpression="set is_verified =:is_verified",
					ExpressionAttributeValues={
						':is_verified':is_verified,
					},
					ReturnValues="UPDATED_NEW"
				)

				email_id = request.session['email_id']
				earnings = request.session['earnings_emp']
				print('============mechanichu===================')
				print(earnings)
				earnings = earnings + 1500
				print(earnings)

				table = dynamodb.Table('Employee')
				response = table.update_item(
					Key={
						'email_id': email_id,
					},
					UpdateExpression="set earnings =:earnings",
					ExpressionAttributeValues={
						':earnings':earnings,
					},
					ReturnValues="UPDATED_NEW"
				)
				request.session['earnings_emp'] = earnings

				table = dynamodb.Table('verifications')
				response = table.scan()
				sr = 0
				if(len(response['Items'])==0):
					sr = 1
				else:
					temp = 0
					for i in response['Items']:
						if temp<int(i['sr']):
							temp = int(i['sr'])
					sr = temp+1
				print(sr)
				response = table.put_item(
					Item = {
						'sr': sr,
						'employee_email':email_id,
						'checked_email':email,
						'type_of': typ,
					}
				)




		email_id = request.session['email_id']
		dynamodb = boto3.resource('dynamodb')
		table = dynamodb.Table('Employee')
		response = table.scan(
			FilterExpression=Attr('email_id').eq(email_id)
		)
		dic = {}
		dic['email_id'] = response['Items'][0]['email_id']
		dic['contact'] = response['Items'][0]['contact']
		dic['verified_count'] =response['Items'][0]['verified_count']
		dic['earnings'] = response['Items'][0]['earnings']

		Cars = []
		table = dynamodb.Table('Car')
		response = table.scan()
		# print('a')
		# print('a')
		# print(response)
		# print('a')
		# print('a')
		for i in response['Items']:
			print(i['car_model'])
			print(i['is_verified'])
			print(type(i['car_model']))
			print(type(i['is_verified']))
			print('b')
			if(i['is_verified'] == False and i['car_model'] != '0'):
				print(i['car_model'])
				Cars.append(i)
		print(Cars)

		Mechanics = []
		table = dynamodb.Table('Mechanic')
		response = table.scan()
		for i in response['Items']:
			if(i['is_verified'] == False):
				Mechanics.append(i)
		#print(Mechanics)
		dic['Cars'] = Cars
		dic['Mechanics'] = Mechanics
		return render(request, 'dashboard/emp.html',dic)
	return redirect('user_dashboard')


def car_details(request, email):
	print(email)
	dic = {}
	dynamodb = boto3.resource('dynamodb')
	table = dynamodb.Table('Car')
	response = table.scan(
		FilterExpression=Attr('email_id').eq(email)
	)

	print('table scan')
	print(response['Items'][0]['co_ordinates'])
	print(type(response['Items'][0]['co_ordinates']))
	print(response['Items'][0]['co_ordinates'][0])
	lat = ""
	long = ""
	temp=0
	for i in response['Items'][0]['co_ordinates'][1:-1]:
		if i==',':
			temp=1
		elif temp==0:
			lat+=i
		else:
			long+=i

	dic['email_id'] = email
	request.session['owner_email'] = email
	dic['car_name'] = response['Items'][0]['car_name']
	dic['car_number'] = response['Items'][0]['car_number']
	request.session['owner_car_number'] = dic['car_number']
	request.session['owner_car_name'] = dic['car_name']

	dic['car_model'] = response['Items'][0]['car_model']
	dic['co_ordinates'] = response['Items'][0]['co_ordinates']

	dic['lat'] = float(lat)
	dic['long'] = float(long)

	print(dic['lat'])

	dic['cost_perday'] = response['Items'][0]['cost_perday']
	dic['is_available'] =  response['Items'][0]['is_available']
	dic['is_verified'] =  response['Items'][0]['is_verified']
	dic['rating'] =  response['Items'][0]['rating']
	dic['earnings'] =  response['Items'][0]['earnings']
	request.session['car_owner_earnings'] = int(response['Items'][0]['earnings'])
	return render(request, 'dashboard/car_details.html',dic)

	# return redirect('home')

def checkout_view(request):
	try:
		request.session['email_id']
	except:
		#return render(request,'dashboard/checkout.html')
		return redirect('login')
	else:
		#return redirect('login')
		email_id = request.session['owner_email']
		cost_perday = request.POST.get('cost_perday')
		print(email_id)
		print("----------------------")
		dic={}
		dic['email_id'] = email_id
		dic['cost_perday'] = cost_perday
		return render(request,'dashboard/checkout.html',dic)


def success_payment(request,value,email):
	try:
		request.session['email_id']
	except:
		#return render(request,'dashboard/checkout.html')
		return redirect('login')
	else:
		dic = {}
		dynamodb = boto3.resource('dynamodb')
		table = dynamodb.Table('Car')

		print(value)
		print("AYYINDI MARI2")
		print(email)
		if value=='yes':
			response = table.scan(
				FilterExpression=Attr('email_id').eq(email)
			)
			earnings = int(response['Items'][0]['earnings']) + int(response['Items'][0]['cost_perday'])
			is_available = False
			response = table.update_item(
				Key={
					'email_id': email,
				},
				UpdateExpression="set earnings = :earnings, is_available =:is_available",
				ExpressionAttributeValues={
					':earnings': earnings,
					':is_available':is_available,
				},
				ReturnValues="UPDATED_NEW"
			)
			owner_email = email
			buyer_email = request.session['email_id']
			car_no = request.session['owner_car_number']
			car_name = request.session['owner_car_name']
			dynamodb = boto3.resource('dynamodb')
			table = dynamodb.Table('bookings')
			response = table.scan()
			sr = 0
			if(len(response['Items'])==0):
				sr = 1
			else:
				temp = 0
				for i in response['Items']:
					if temp<int(i['sr']):
						temp = int(i['sr'])
				sr = temp+1
			print(sr)
			response = table.put_item(
				Item = {
					'sr': sr,
					'owner_email':owner_email,
					'buyer_email':buyer_email,
					'car_number': car_no,
					'car_name' : car_name,
				}
			)
		return redirect('home')
