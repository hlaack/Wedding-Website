from django.conf import settings
from django.shortcuts import render
from .models import Family, Person
import os
from functools import wraps
from django.http import HttpResponseRedirect
from django.urls import reverse
import logging
from django_ratelimit.decorators import ratelimit
from pathlib import Path

logger = logging.getLogger(__name__)

def rsvp_authenticated_required(view_func):
    """Decorator to check if user has entered correct RSVP password"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.session.get('rsvp_authenticated'):
            return HttpResponseRedirect(reverse('password_entry'))
        return view_func(request, *args, **kwargs)
    return wrapper

def index(request):
    return render(request, 'index.html')

def people(request):
    return render(request, 'people.html')

def photos(request):
    """Securely list engagement photos without exposing directory traversal vulnerabilities."""
    # Allowed image file extensions
    ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}
    
    photos_dir = Path(settings.BASE_DIR) / "rsvp" / "static" / "images" / "engagement_photos"
    
    # Validate directory exists
    if not photos_dir.exists() or not photos_dir.is_dir():
        logger.warning(f"Photos directory not found: {photos_dir}")
        context_dict_photos = {'files': []}
        return render(request, 'photos.html', context_dict_photos)
    
    try:
        # List only files (not directories) with allowed extensions
        secure_files = []
        for item in photos_dir.iterdir():
            # Skip directories and hidden files
            if item.is_file() and not item.name.startswith('.'):
                # Only include whitelisted image extensions
                if item.suffix.lower() in ALLOWED_EXTENSIONS:
                    # Store only the filename, not the full path (prevents path traversal)
                    secure_files.append(item.name)
        
        secure_files.sort()  # Sort alphabetically for consistent display
        context_dict_photos = {'files': secure_files}
        logger.debug(f"Loaded {len(secure_files)} photos from engagement_photos directory")
        
    except PermissionError:
        logger.error(f"Permission denied accessing photos directory: {photos_dir}")
        context_dict_photos = {'files': []}
    except Exception as e:
        logger.error(f"Error loading photos: {str(e)}")
        context_dict_photos = {'files': []}
    
    return render(request, 'photos.html', context_dict_photos)

# def password_entry(request):
#     return render(request, 'password_entry.html')

# def rsvp(request):
#     return render(request, 'rsvp.html')

from django.shortcuts import get_object_or_404
from .forms import PasswordEntryForm, RsvpQueryForm, RsvpPersonSelectForm
from django.contrib import messages

@ratelimit(key='ip', rate='5/5m', method='POST', block=True)
def rsvp_password_entry(request):
    """Handle RSVP password entry with rate limiting to prevent brute force attacks."""
    # If already authenticated, redirect to rsvp page
    if request.session.get('rsvp_authenticated'):
        return HttpResponseRedirect(reverse('rsvp'))

    if request.method == 'POST':
        form = PasswordEntryForm(request.POST)

        if form.is_valid():
            request.session['rsvp_authenticated'] = True
            logger.info(f"Successful RSVP authentication from IP: {get_client_ip(request)}")
            return HttpResponseRedirect(reverse('rsvp'))
        else:
            # Log failed authentication attempts
            logger.warning(f"Failed RSVP authentication attempt from IP: {get_client_ip(request)}")
            # Generic message - don't reveal if password is wrong
            form.add_error(None, "Invalid password. Please try again.")

    else:
        form = PasswordEntryForm()

    return render(request, 'password_entry.html', {'form': form})

def get_client_ip(request):
    """Extract client IP address from request, accounting for proxies."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
        
@rsvp_authenticated_required
def rsvp_page(request):

    for key in ['entered_email', 'entered_phone_num']:
        request.session.pop(key, None)

    if request.method == 'POST':

        form = RsvpQueryForm(request.POST)

        last_name = request.POST.get('entered_last_name')
        #url = reverse('rsvp_select')

        if form.is_valid():

            families = Family.objects.filter(family_name__iexact=last_name)
            email = form.cleaned_data['entered_email']
            phone_num = form.cleaned_data['entered_phone_num']

            # Generic error if no families found (prevents user enumeration)
            if families.count() == 0:
                logger.info(f"RSVP lookup attempt for non-existent family: {last_name}")
                # Add error to last_name field so it displays where user can see it
                form.add_error('entered_last_name', "We couldn't find your information. Please check your entry and try again.")
                return render(request, 'rsvp.html', {'form': form})

            if families.count() > 1:
                request.session['entered_email'] = email
                request.session['entered_phone_num'] = str(phone_num)
                return HttpResponseRedirect(f"{reverse('rsvp_family_select')}?last_name={last_name}")

            family = families.first()
            family.email = email
            family.phone_number = phone_num
            family.save()

            personName = form.cleaned_data['entered_first_name']
            messages.success(request, personName)
            return HttpResponseRedirect(f"{reverse('rsvp_select')}?family_id={family.familyID}")
        
    else:
        form = RsvpQueryForm()

    return render(request, 'rsvp.html', {'form': form})

@rsvp_authenticated_required
def rsvp_select(request):

    #last_name = request.GET.get('last_name') or request.POST.get('last_name')
    family_id = request.GET.get('family_id') or request.POST.get('family_id')
    family = get_object_or_404(Family, familyID=family_id)
    family_id = request.GET.get('family_id') or request.POST.get('family_id')
    family = get_object_or_404(Family, familyID=family_id)

    if request.method == 'POST':
        form = RsvpPersonSelectForm(request.POST, family=family)
        if form.is_valid():
            selected_people = form.cleaned_data['people']

            for person in family.people.all():
                if person in selected_people:
                    person.status = 'y'
                if person not in selected_people:
                    person.status = 'n'
                person.save()

            return HttpResponseRedirect(reverse('rsvp_confirmation'))

    else:
        form = RsvpPersonSelectForm(family=family)

    return render(request, 'rsvp_select.html', {'form' : form, 'family' : family})

@rsvp_authenticated_required
def rsvp_confirmation(request):

    return render(request, 'rsvp_confirmation.html')

@rsvp_authenticated_required
def rsvp_family_select(request):

    #TODO:
    last_name = request.GET.get('last_name')
    families = Family.objects.filter(family_name__iexact=last_name)

    if request.method == 'POST':
        family_id = request.POST.get('family_id')
        family = get_object_or_404(Family, familyID=family_id)

        email = request.session.get('entered_email')
        phone = request.session.get('entered_phone_num')

        if email:
            family.email = email
        if phone:
            family.phone_number = phone
        family.save()

        for key in ['entered_email', 'entered_phone_num']:
            if key in request.session:
                del request.session[key]

        return HttpResponseRedirect(f"{reverse('rsvp_select')}?family_id={family.familyID}")

    return render(request, 'rsvp_family_select.html', {'families': families})

def place(request):

    return render(request, 'place.html')

def travel(request):
    
    return render(request, 'travel.html')

def questions(request):
    
    return render(request, 'questions.html')

def registry(request):
    
    return render(request, 'registry.html')
