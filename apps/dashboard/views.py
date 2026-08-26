from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return render(request, "dashboard/home.html")

def hello(request):
    return HttpResponse("<strong>Hello from HTMX!</strong>")