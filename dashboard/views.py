from django.shortcuts import render

def home_view(request):
	context = {}
	return render(request, 'home.html', context)

def dashboard_view(request):
	context = {}
	context['udata'] = {'name': "Rishabh Tripath", 'age': 20, 'gender': 'M', 'dLicense': "1233456", 'email_id': "rishabh@gmail.com", 'username': "rt134"}
	return render(request,'templates/dashboard.html', context)

def car_view(request):
	context = dict()
	context['carlist'] = [{'car_name': "Innova", "img": "https://imgd.aeplcdn.com/1056x594/n/cw/ec/20623/innova-crysta-exterior-right-front-three-quarter.jpeg?q=85"},
						{'car_name': "4 Matic", "img": "https://imgd.aeplcdn.com/1056x594/cw/ec/20442/Mercedes-Benz-GLE-Class-Right-Front-Three-Quarter-58803.jpg?v=201711021421&q=85"},
						{'car_name': "Jaguar Xf", "img": "https://imgd.aeplcdn.com/1056x594/cw/ec/19826/Jaguar-XF-Right-Front-Three-Quarter-80407.jpg?v=201711021421&q=85"},
						{'car_name': "Dicovery", "img": "https://imgd.aeplcdn.com/1056x594/n/cw/ec/44879/landrover-discovery-sport-front-view15.jpeg?q=85"},
						{'car_name': "Mustang", "img": "https://imgd.aeplcdn.com/1056x594/n/cw/ec/49098/mustang-facelift-exterior-left-rear-three-quarter.jpeg?q=85"},
						{'car_name': "Jeep compass", "img": "https://imgd.aeplcdn.com/1056x594/n/cw/ec/25107/compass-exterior-left-front-three-quarter-3.jpeg?q=85"},
						{'car_name': "XUV 500", "img": "https://imgd.aeplcdn.com/1056x594/n/cw/ec/34024/xuv500-exterior-left-front-three-quarter.jpeg?q=85"}]
	return render(request,'templates/car.html', context)

def mechanic_view(request):
	context = dict()
	context['mechaniclist'] = [{'car_name': "Ramesh", "img": "https://cdn5.vectorstock.com/i/1000x1000/64/94/creative-gear-wrench-monochrome-label-logo-design-vector-25456494.jpg"},
						{'car_name': "Suresh", "img": "https://cdn2.vectorstock.com/i/1000x1000/65/26/creative-mechanic-gear-hand-wrench-logo-design-vector-25456526.jpg"},
						{'car_name': "Dinesh", "img": "https://cdn4.vectorstock.com/i/1000x1000/65/23/creative-mechanic-gear-hand-wrench-logo-design-vector-25456523.jpg"},
						{'car_name': "Mahesh", "img": "https://cdn4.vectorstock.com/i/1000x1000/64/23/creative-fist-mechanic-wrench-gear-logo-vector-25456423.jpg"},
						{'car_name': "Ganesh", "img": "https://cdn2.vectorstock.com/i/1000x1000/64/21/creative-gear-wrench-logo-design-vector-25456421.jpg"},
						{'car_name': "Deepesh", "img": "https://cdn5.vectorstock.com/i/1000x1000/64/94/creative-gear-wrench-monochrome-label-logo-design-vector-25456494.jpg"},
						{'car_name': "Pritesh", "img": "https://cdn2.vectorstock.com/i/1000x1000/64/21/creative-gear-wrench-logo-design-vector-25456421.jpg"}]
	return render(request,'templates/mechanic.html', context)