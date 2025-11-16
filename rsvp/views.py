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
from .forms import PasswordEntryForm, RsvpQueryForm, RsvpPersonSelectForm
from django.contrib import messages

def rsvp_password_entry(request):

    if request.method == 'POST':

        form = PasswordEntryForm(request.POST)

        if form.is_valid():
            return HttpResponseRedirect(reverse('rsvp'))

    else:
        form = PasswordEntryForm()

    return render(request, 'password_entry.html', {'form': form})
        
def rsvp_page(request):

    for key in ['entered_email', 'entered_phone_num']:
        request.session.pop(key, None)

    if request.method == 'POST':

        form = RsvpQueryForm(request.POST)

        last_name = request.POST.get('entered_last_name')
        #url = reverse('rsvp_select')

        if form.is_valid():

            families = Family.objects.filter(family_name__iexact=last_name)
            #family = get_object_or_404(Family, family_name__iexact=last_name)
            email = form.cleaned_data['entered_email']
            phone_num = form.cleaned_data['entered_phone_num']

            if families.count() > 1:
                request.session['entered_email'] = email
                request.session['entered_phone_num'] = str(phone_num)
                return HttpResponseRedirect(f"{reverse('rsvp_family_select')}?last_name={last_name}")
                #TODO: CREATE RSVP_FAMILY_SELECT PAGE

            family = families.first()

            family.email = email
            family.phone_number = phone_num
            family.save()

            #TODO: CHECK IF MULTIPLE OF LAST NAME, THEN REDIRECT TO SELECT

            personName = form.cleaned_data['entered_first_name']
            messages.success(request, personName)
            return HttpResponseRedirect(f"{reverse('rsvp_select')}?family_id={family.familyID}")
        
    else:
        form = RsvpQueryForm()

    return render(request, 'rsvp.html', {'form': form})

def rsvp_select(request):

    #last_name = request.GET.get('last_name') or request.POST.get('last_name')
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

def rsvp_confirmation(request):

    return render(request, 'rsvp_confirmation.html')

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
