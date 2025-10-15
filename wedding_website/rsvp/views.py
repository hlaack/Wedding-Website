from django.shortcuts import render
from .models import Family, Person

def index(request):
    return render(request, 'index.html')

def people(request):
    return render(request, 'people.html')

def photos(request):
    return render(request, 'photos.html')

# def password_entry(request):
#     return render(request, 'password_entry.html')

# def rsvp(request):
#     return render(request, 'rsvp.html')

from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import PasswordEntryForm

def rsvp_password_entry(request):

    if request.method == 'POST':

        form = PasswordEntryForm(request.POST)

        if form.is_valid():
            return HttpResponseRedirect(reverse('rsvp'))

    else:
        form = PasswordEntryForm()

    return render(request, 'password_entry.html', {'form': form})
        
def rsvp_page(request):
    return render(request, 'rsvp.html')



