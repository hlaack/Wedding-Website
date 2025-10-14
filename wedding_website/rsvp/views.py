from django.shortcuts import render
from .models import Family, Person

def index(request):
    return render(request, 'index.html')

def people(request):
    return render(request, 'people.html')

def photos(request):
    return render(request, 'photos.html')

def password_entry(request):
    return render(request, 'password_entry.html')