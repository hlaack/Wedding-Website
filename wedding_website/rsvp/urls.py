from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('people.html', views.people, name='people'),
    path('index.html', views.index, name='index'),
    path('photos.html', views.photos, name='photos'),
    path('password_entry.html', views.rsvp_password_entry, name='password_entry'),
    path('rsvp.html', views.rsvp_page, name='rsvp')
]