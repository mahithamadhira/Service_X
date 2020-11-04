from django.shortcuts import render
import boto3
from boto3.dynamodb.conditions import Key, Attr

# Create your views here.
def home(request):
    return render(request,'home/home.html')
def home_view(request):
	dynamodb = boto3.resource('dynamodb')
	table = dynamodb.Table('User')
	last_name = "kikkuri"
	response = table.put_item(
	            Item={
	                'email_id': "jaffa@iiits.in",
	                'username': "iam_jaffa",
					"fname": "jaffa",
					"lname": last_name,
	            }
	        )
	#print(response)
	response = table.scan()
	print(response)
	#print(response['Items'])
	#for i in response['Items']:
	#	print(i['email_id'])
	response = table.scan(
        ProjectionExpression='username',
        FilterExpression=Attr('email_id').eq('jaffa@iiits.in')
    )
	print(response)
	print(response['Items'])
	return render(request,'home/home.html')
