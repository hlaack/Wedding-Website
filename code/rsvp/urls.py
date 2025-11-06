from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('people.html', views.people, name='people'),
    path('index.html', views.index, name='index'),
    path('photos.html', views.photos, name='photos'),
    path('password_entry.html', views.rsvp_password_entry, name='password_entry'),
    path('rsvp.html', views.rsvp_page, name='rsvp'),
    path('rsvp_select.html', views.rsvp_select, name='rsvp_select'),
    path('rsvp_confirmation.html', views.rsvp_confirmation, name='rsvp_confirmation'),
    path('rsvp_family_select.html', views.rsvp_family_select, name='rsvp_family_select'),
    path('place.html', views.place, name='place'),
    path('travel.html', views.travel, name='travel'),
]
