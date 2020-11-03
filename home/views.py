from django.shortcuts import render
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
	return render(request, 'home/home.html')
