from django.shortcuts import render, redirect
from django.contrib import sessions
import boto3
from boto3.dynamodb.conditions import Key, Attr
from django.core.files.storage import FileSystemStorage

# Create your views here.
#def home_view(request):
	# myfile = request.FILES['sentFile']
	# fs = FileSystemStorage()
	# filename = fs.save(myfile.name, myfile)
	# f = request.FILES['sentFile']
	# f="./media/"+str(myfile)
	# s3 = boto3.client('s3')
	# bucket = 'proof_imgs'
	#
	# file_name = str(f)
	# key_name = str(myfile)
	#
	# s3.upload_file(file_name, bucket, key_name)
	#
	# bucket_location = boto3.client('s3').get_bucket_location(Bucket=bucket)
	# link = "https://s3-ap-south-1.amazonaws.com/{0}/{1}".format(bucket,key_name)
	# print(link)
	# dynamodb = boto3.resource('dynamodb')
	# table = dynamodb.Table('User')
	# last_name = "kikkuri"
	# response = table.put_item(
	#             Item={
	#                 'email_id': email,
	#                 'username': user_name,
	# 				"fname": f_name,
	# 				"lname": l_name,
	#             }
	#         )
	# #print(response)
	# response = table.scan()
	# print(response)
	# #print(response['Items'])
	# #for i in response['Items']:
	# #	print(i['email_id'])
	# response = table.scan(
    #     ProjectionExpression='username',
    #     FilterExpression=Attr('email_id').eq('jaffa@iiits.in')
    # )
	# print(response)
	# print(response['Items'])
	# return render(request,'home/home.html')

def home_view(request):
	try:
		request.session['email_id']
		print(request.session['email_id'])

		dic = {}
		dynamodb = boto3.resource('dynamodb')
		table = dynamodb.Table('Car')
		response = table.scan()
		lat = []
		long = []
		emails = []
		names=[]
		print('try')
		print(response['Items'])

		for j in response['Items']:
			temp=0
			lat1 = ""
			long1 = ""
			if j['co_ordinates'] != '-' and j['is_available']==True and j['email_id']!=request.session['email_id']:
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
				names.append(j['car_name'])
				emails.append(j['email_id'])
		print(lat)
		print(type(lat))
		dic['lat'] = lat
		dic['long'] = long
		dic['names'] = names
		dic['emails'] = emails

	except:
		# dic = {}
		# dynamodb = boto3.resource('dynamodb')
		# table = dynamodb.Table('Car')
		# response = table.scan()
		# lat = []
		# long = []
		# emails = []
		# names=[]
		# print('except')
		# print(response['Items'])
		# for j in response['Items']:
		# 	temp=0
		# 	lat1 = ""
		# 	long1 = ""
		# 	if j['co_ordinates'] != '-' and j['is_available']==True  and j['email_id']!=request.session['email_id']:
		# 		for i in j['co_ordinates'][1:-1]:
		# 			if i==',':
		# 				temp=1
		# 			elif temp==0:
		# 				lat1+=i
		# 			else:
		# 				long1+=i
		# 		print(lat1)
		# 		print(type(lat1))
		# 		print(long1)
		# 		print(type(long1))
		# 		lat1 = float(lat1)
		# 		long1 = float(long1)
		# 		lat.append(lat1)
		# 		long.append(long1)
		# 		names.append(j['car_name'])
		# 		emails.append(j['email_id'])
		#
		# print(lat)
		# print(type(lat))
		# dic['lat'] = lat
		# dic['long'] = long
		# dic['names'] = names
		# dic['emails'] = emails
		#
		# return render(request, 'home/home.html', dic)

		return render(request, 'home/home.html')
	finally:
		if 'email_id' in request.session:
			dic = {}
			dynamodb = boto3.resource('dynamodb')
			table = dynamodb.Table('Car')
			response = table.scan()
			lat = []
			long = []
			emails = []
			names=[]
			print('finally')
			print(response['Items'])
			for j in response['Items']:
				temp=0
				lat1 = ""
				long1 = ""
				if j['co_ordinates'] != '-' and j['is_available']==True and j['email_id']!=request.session['email_id']:
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
					names.append(j['car_name'])
					emails.append(j['email_id'])

			print(lat)
			print(type(lat))
			dic['lat'] = lat
			dic['long'] = long
			dic['names'] = names
			dic['emails'] = emails
			return render(request, 'home/home2.html',dic)
		else:
			return render(request, 'home/home.html')
