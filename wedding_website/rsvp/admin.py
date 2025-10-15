from django.contrib import admin

from .models import Family, Person, RSVP_Protector

admin.site.register(Family)
admin.site.register(Person)
admin.site.register(RSVP_Protector)
