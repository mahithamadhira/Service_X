from django.shortcuts import render, redirect
from django.contrib import sessions
import boto3
from boto3.dynamodb.conditions import Key, Attr
from django.contrib import sessions
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.core.files.storage import FileSystemStorage
from telesign.messaging import MessagingClient
import requests
import json

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
		try:
			myfile = request.FILES['sentFile']
			fs = FileSystemStorage()
			filename = fs.save(myfile.name, myfile)
			f = request.FILES['sentFile']
			f="./media/"+str(myfile)
			s3 = boto3.client('s3')
			bucket = 'servicex12'

			file_name = str(f)
			key_name = str(myfile)

			s3.upload_file(file_name, bucket, key_name)

			bucket_location = boto3.client('s3').get_bucket_location(Bucket=bucket)
			link = "https://s3-ap-south-1.amazonaws.com/{0}/{1}".format(bucket,key_name)
		except:
			print('except')
			dynamodb = boto3.resource('dynamodb')
			table = dynamodb.Table('User')
			response = table.scan(
				FilterExpression=Attr('email_id').eq(email_id)
			)
			link = response['Items'][0]['img']

		finally:
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

				print(f"link : {link} \n")
				response = table.update_item(
				Key={
					'email_id': email_id,
				},
				UpdateExpression="set fname=:fname, lname=:lname, username =:username, gender =:gender, age =:age, is_admin =:is_admin, is_staff =:is_staff, contact =:contact, dLicense = :dLicense, img=:img",
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
					':img':link,
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
				dic['img'] = response['Items'][0]['img']
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
			dic['img'] = response['Items'][0]['img']

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
		dic = {}
		dynamodb = boto3.resource('dynamodb')
		table = dynamodb.Table('mBooking')
		response = table.scan()
		email = request.session['email_id']
		print(email)
		buy_email = []
		for i in response['Items']:
			if i['mech_email'] == email:
				buy_email.append(i['buyer_email'])

		dynamodb = boto3.resource('dynamodb')
		table = dynamodb.Table('User')
		response = table.scan()



		# contact = []
		# email_buyer = []
		final = []
		for i in response['Items']:
			if i['email_id'] in buy_email:
				result = {}
				result['email_buyer'] = i['email_id']
				result['contact'] = i['contact']
				final.append(result)

				# email_buyer.append(i['email_id'])
				# contact.append(i['contact'])


		dic['buyer_details_contact'] = final
		print(dic)
		return render(request, 'dashboard/mech_earn.html',dic)

	return redirect('user_dashboard')





def tandc(request):
	return render(request, "dashboard/tandc.html")





def user_took(request):
	if request.method== 'POST':
		email_id = request.POST.get('email_id')
		dynamodb = boto3.resource('dynamodb')
		table = dynamodb.Table('Car')
		is_available = True
		response = table.scan(
			FilterExpression=Attr('email_id').eq(email_id)
		)
		response = table.update_item(
		Key={
			'email_id': email_id,
		},
		UpdateExpression="set is_available = :is_available",
		ExpressionAttributeValues={
			':is_available':is_available,
		},
		ReturnValues="UPDATED_NEW"
		)
	dic = {}
	took_cars = []
	price = []
	email = request.session['email_id']
	dynamodb = boto3.resource('dynamodb')
	table = dynamodb.Table('bookings')
	response = table.scan(
		FilterExpression=Attr('buyer_email').eq(email)
	)
	for i in response['Items']:
		print(i['owner_email'])
		owner_email = i['owner_email']
		table1 = dynamodb.Table('Car')
		response = table1.scan(
			FilterExpression=Attr('email_id').eq(owner_email)
		)
		img = response['Items'][0]['img']
		i['img'] = img
		print(i['img'])
		took_cars.append(i)
	dic['took_cars'] =  took_cars


	dynamodb = boto3.resource('dynamodb')
	table = dynamodb.Table('mBooking')
	response = table.scan()

	mec_email = []
	for i in response['Items']:
		if i['buyer_email'] == email:
			mec_email.append(i['mech_email'])

	dynamodb = boto3.resource('dynamodb')
	table = dynamodb.Table('User')
	response = table.scan()



	# contact = []
	# email_buyer = []
	final = []
	for i in response['Items']:
		if i['email_id'] in mec_email:
			result = {}
			result['email_mech'] = i['email_id']
			result['contact'] = i['contact']
			final.append(result)

			# email_buyer.append(i['email_id'])
			# contact.append(i['contact'])


	dic['buyer_details_contact'] = final
	print(dic)



	return render(request,'dashboard/took_car.html',dic)

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
			try:
				myfile = request.FILES['sentFile']
				fs = FileSystemStorage()
				filename = fs.save(myfile.name, myfile)
				f = request.FILES['sentFile']
				f="./media/"+str(myfile)
				s3 = boto3.client('s3')
				bucket = 'servicex12'

				file_name = str(f)
				key_name = str(myfile)

				s3.upload_file(file_name, bucket, key_name)

				bucket_location = boto3.client('s3').get_bucket_location(Bucket=bucket)
				link = "https://s3-ap-south-1.amazonaws.com/{0}/{1}".format(bucket,key_name)
			except:
				print('except')
				dynamodb = boto3.resource('dynamodb')
				table = dynamodb.Table('Car')
				response = table.scan(
					FilterExpression=Attr('email_id').eq(email_id)
				)
				link = response['Items'][0]['img']

			finally:
				print(link)
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
					UpdateExpression="set car_name=:car_name, car_number=:car_number, car_model =:car_model, co_ordinates =:co_ordinates, cost_perday = :cost_perday, is_available =:is_available, img =:img",
					ExpressionAttributeValues={
						':car_name': car_name,
						':car_number': car_number,
						':car_model': car_model,
						':co_ordinates':co_ordinates,
						':cost_perday':cost_perday,
						':is_available':is_available,
						':img':link,
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
				# dic['link'] = response['Items'][0]['img']
				dic['earnings'] =  response['Items'][0]['earnings']
				print('ayyindi mari')


				dynamodb = boto3.resource('dynamodb')
				table = dynamodb.Table('bookings')
				response = table.scan()

				buy_email = []
				for i in response['Items']:
					if i['owner_email'] == email_id:
						buy_email.append(i['buyer_email'])

				dynamodb = boto3.resource('dynamodb')
				table = dynamodb.Table('User')
				response = table.scan()



				# contact = []
				# email_buyer = []
				final = []
				for i in response['Items']:
					if i['email_id'] in buy_email:
						result = {}
						result['email_buyer'] = i['email_id']
						result['contact'] = i['contact']
						final.append(result)

						# email_buyer.append(i['email_id'])
						# contact.append(i['contact'])


				dic['buyer_details_contact'] = final
				print(dic)

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

		# if(response['Items'][0]['cost_perday'] == 0):
		# 	dic['cost_perday']=""
		# else:
		# 	dic['cost_perday'] = response['Items'][0]['cost_perday']

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
		# dic['link'] = response['Items'][0]['img']
		dic['earnings'] =  response['Items'][0]['earnings']


		dynamodb = boto3.resource('dynamodb')
		table = dynamodb.Table('bookings')
		response = table.scan()

		buy_email = []
		for i in response['Items']:
			if i['owner_email'] == email:
				buy_email.append(i['buyer_email'])

		dynamodb = boto3.resource('dynamodb')
		table = dynamodb.Table('User')
		response = table.scan()



		# contact = []
		# email_buyer = []
		final = []
		for i in response['Items']:
			if i['email_id'] in buy_email:
				result = {}
				result['email_buyer'] = i['email_id']
				result['contact'] = i['contact']
				final.append(result)

				# email_buyer.append(i['email_id'])
				# contact.append(i['contact'])


		dic['buyer_details_contact'] = final
		print(dic)

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
			g_name = request.POST.get('g_name')
			#is_verified = request.session['is_verified']
			#rating = request.session['rating']
			lat = request.POST.get('lat')
			long = request.POST.get('long')
			print(g_name)
			co_ordinates = '['
			co_ordinates+=lat
			co_ordinates+=','
			co_ordinates+=long
			co_ordinates+=']'
			try:
				myfile = request.FILES['sentFile']
				fs = FileSystemStorage()
				filename = fs.save(myfile.name, myfile)
				f = request.FILES['sentFile']
				f="./media/"+str(myfile)
				s3 = boto3.client('s3')
				bucket = 'servicex12'

				file_name = str(f)
				key_name = str(myfile)

				s3.upload_file(file_name, bucket, key_name)

				bucket_location = boto3.client('s3').get_bucket_location(Bucket=bucket)
				link = "https://s3-ap-south-1.amazonaws.com/{0}/{1}".format(bucket,key_name)
			except:
				print('except')
				dynamodb = boto3.resource('dynamodb')
				table = dynamodb.Table('User')
				response = table.scan(
					FilterExpression=Attr('email_id').eq(email_id)
				)
				link = response['Items'][0]['img']
			finally:
				if(is_available == 'true'):
					is_available = 'True'
				else:
					is_available = 'False'
				# if(co_ordinates == '-'):
				# 	 messages.success(request, 'Please put the location of your shed')
				# if(service_charge == 0):
				# 	 messages.success(request, 'You can give services for free!')
				if(co_ordinates != '[17.18,87.14]' and service_charge!=0):
					dynamodb = boto3.resource('dynamodb')
					table = dynamodb.Table('Mechanic')
					response = table.update_item(
						Key={
							'email_id': email_id,
						},
						UpdateExpression="set co_ordinates=:co_ordinates, service_charge=:service_charge, is_available =:is_available, img = :img, g_name = :g_name",
						ExpressionAttributeValues={
							':co_ordinates': co_ordinates,
							':service_charge': service_charge,
							':is_available':is_available,
							':img': link,
							':g_name':g_name,
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
				print(response['Items'])
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
				dic['g_name'] = response['Items'][0]['g_name']
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
			print(response['Items'])
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

			#
			# dynamodb = boto3.resource('dynamodb')
			# table = dynamodb.Table('mBooking')
			# response = table.scan()
			# email = request.session['email_id']
			# print(email)
			# buy_email = []
			# for i in response['Items']:
			# 	if i['mech_email'] == email:
			# 		buy_email.append(i['buyer_email'])
			#
			# dynamodb = boto3.resource('dynamodb')
			# table = dynamodb.Table('User')
			# response = table.scan()
			#
			#
			#
			# # contact = []
			# # email_buyer = []
			# final = []
			# for i in response['Items']:
			# 	if i['email_id'] in buy_email:
			# 		result = {}
			# 		result['email_buyer'] = i['email_id']
			# 		result['contact'] = i['contact']
			# 		final.append(result)
			#
			# 		# email_buyer.append(i['email_id'])
			# 		# contact.append(i['contact'])
			#
			#
			# dic['buyer_details_contact'] = final
			# print(dic)
			#


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
			if(i['is_verified'] == False and i['car_model'] != '0' and i['co_ordinates']!='-'):
				print(i['car_model'])
				Cars.append(i)
		print(Cars)

		Mechanics = []
		table = dynamodb.Table('Mechanic')
		response = table.scan()
		for i in response['Items']:
			if(i['is_verified'] == False and i['co_ordinates']!='-' and i['service_charge']!=0):
				Mechanics.append(i)
		#print(Mechanics)
		dic['Cars'] = Cars
		dic['Mechanics'] = Mechanics
		return render(request, 'dashboard/emp.html',dic)
	return redirect('user_dashboard')



def mechanic_booking(request):
	dic = {}
	dynamodb = boto3.resource('dynamodb')
	table = dynamodb.Table('Mechanic')
	response = table.scan()
	lat = []
	long = []
	emails = []
	names=[]
	print('try')
	print(response['Items'])

	for j in response['Items']:
		print(j['co_ordinates'])
		print("--------------------------------")
		temp=0
		lat1 = ""
		long1 = ""
		if j['co_ordinates'] != '-' and (j['is_available']==True or j['is_available']=="True" or j['is_available']=="true") and j['email_id']!=request.session['email_id']:
			print(j['co_ordinates'])
			for i in j['co_ordinates'][1:-1]:
				if i==',':
					temp=1
				elif temp==0:
					lat1+=i
				else:
					long1+=i
			print(lat1)
			print(type(lat1))
			print(long1)
			print(type(long1))
			lat1 = float(lat1)
			long1 = float(long1)
			lat.append(lat1)
			long.append(long1)
			names.append(j['g_name'])
			emails.append(j['email_id'])
	print(lat)
	print(type(lat))
	dic['lat'] = lat
	dic['long'] = long
	dic['names'] = names
	dic['emails'] = emails
	print(dic)

	return render(request,'dashboard/mech_book.html', dic)






def mech_details(request, email):
	print(email)
	dic = {}
	dynamodb = boto3.resource('dynamodb')
	table = dynamodb.Table('Mechanic')
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
	request.session['mech_email'] = email
	dic['img'] = response['Items'][0]['img']
	dic['g_name'] = response['Items'][0]['g_name']
	dic['service_charge'] = response['Items'][0]['service_charge']

	dic['co_ordinates'] = response['Items'][0]['co_ordinates']

	dic['lat'] = float(lat)
	dic['long'] = float(long)
	print(dic)
	print(dic['lat'])

	# dic['cost_perday'] = response['Items'][0]['cost_perday']
	# dic['is_available'] =  response['Items'][0]['is_available']
	# dic['is_verified'] =  response['Items'][0]['is_verified']
	# dic['rating'] =  response['Items'][0]['rating']
	# dic['earnings'] =  response['Items'][0]['earnings']
	# request.session['car_owner_earnings'] = int(response['Items'][0]['earnings'])
	return render(request, 'dashboard/mech_details.html',dic)

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
	dic['img'] = response['Items'][0]['img']
	request.session['car_owner_earnings'] = int(response['Items'][0]['earnings'])
	return render(request, 'dashboard/car_details.html',dic)

	# return redirect('home')


def mech_checkout_view(request):
	try:
		request.session['email_id']
	except:
		#return render(request,'dashboard/checkout.html')
		return redirect('login')
	else:
		#return redirect('login')
		email_id = request.session['mech_email']
		cost_perday = request.POST.get('service_charge')
		print(email_id)
		print("----------------------")
		dic={}
		dic['email_id'] = email_id
		dic['cost_perday'] = cost_perday
		return render(request,'dashboard/checkout.html',dic)




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
		print('dont dont dont')
		if 'owner_email' in request.session and 'mech_email' not in request.session:
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
				status = "not_gib"
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
						'status':status,
					}
				)

				table = dynamodb.Table('User')
				response = table.scan(
					FilterExpression=Attr('email_id').eq(owner_email)
				)
				contact = response['Items'][0]['contact']
				print(contact)
				print(type(contact))
				print(len(contact))
				url = "https://www.fast2sms.com/dev/bulk"

				querystring = {
				"authorization":"9RICC43rcTNq2aVFBbrfzmtVCFXjs6SzZs3s8tOOFxUmBkPj4KGsFiFUfdA8",
				"sender_id":"FSTSMS",
				"message":"Your car has been booked",
				"language":"english",
				"route":"p",
				"numbers":str(contact),
				}

				# headers = {
				#     'cache-control': "no-cache"
				# }

				# response = requests.request("GET", url, headers=headers, params=querystring)
				response = requests.get(url, params=querystring)
		else:
			if value=='yes':
				# car_no = request.session['owner_car_number']
				mech_email = request.session['mech_email']
				buyer_email = request.session['email_id']
				dynamodb = boto3.resource('dynamodb')
				table = dynamodb.Table('Mechanic')
				response = table.scan(
					FilterExpression=Attr('email_id').eq(mech_email)
				)
				earnings = int(response['Items'][0]['earnings']) + int(response['Items'][0]['service_charge'])
				response = table.update_item(
					Key={
						'email_id': mech_email,
					},
					UpdateExpression="set earnings = :earnings",
					ExpressionAttributeValues={
						':earnings': earnings,
					},
					ReturnValues="UPDATED_NEW"
				)


				status = "avail"
				dynamodb = boto3.resource('dynamodb')
				table = dynamodb.Table('mBooking')
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
				sr = str(sr)
				response = table.put_item(
					Item = {
						'sr': sr,
						'mech_email':mech_email,
						'buyer_email':buyer_email,
						'status':status,
					}
				)
				table = dynamodb.Table('User')
				response = table.scan(
					FilterExpression=Attr('email_id').eq(mech_email)
				)
				contact = response['Items'][0]['contact']
				print(contact)
				print(type(contact))
				print(len(contact))
				url = "https://www.fast2sms.com/dev/bulk"

				querystring = {
				"authorization":"9RICC43rcTNq2aVFBbrfzmtVCFXjs6SzZs3s8tOOFxUmBkPj4KGsFiFUfdA8",
				"sender_id":"FSTSMS",
				"message":"You are booked!",
				"language":"english",
				"route":"p",
				"numbers":str(contact),
				}

				# headers = {
				#     'cache-control': "no-cache"
				# }

				# response = requests.request("GET", url, headers=headers, params=querystring)
				response = requests.get(url, params=querystring)


		return redirect('home')
