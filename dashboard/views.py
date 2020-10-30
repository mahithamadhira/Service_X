from django.shortcuts import render

# Create your views here.
def mech_dashboard(request):
	return render(request,'dashboard/mech.html')

def user_dashboard(request):
	return render(request,'dashboard/user.html')

def employee_dashboard(request):
	return render(request,'dashboard/emp.html')

def employee_earnings(request):
	return render(request,'dashboard/emp_earn.html')

def mech_earnings(request):
	return render(request,'dashboard/mech_earn.html')

def user_transactions(request):
	return render(request,'dashboard/user_earn.html')