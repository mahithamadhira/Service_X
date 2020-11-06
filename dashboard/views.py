from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def dashboard(request):
    context=('a'':''a')
    return render(request, 'index.html')