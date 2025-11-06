from django.db import models

import uuid

from django.urls import reverse # Used in get_absolute_url() to get URL for specified ID
from django.db.models import UniqueConstraint # Constrains fields to unique values
from django.db.models.functions import Lower # Returns lower cased value of field

from phonenumber_field.modelfields import PhoneNumberField

class RSVP_Protector(models.Model):
    password = models.CharField(
        max_length=15,
        help_text="Set an RSVP Password.",
        unique=True,
    )

class Family(models.Model):
    #Model representing a family unit.

    familyID = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        help_text="Unique Family ID for this particular family."
    )

    family_name = models.CharField(
        max_length=20,
        help_text="Enter the family last name."
    )

    phone_number = PhoneNumberField(
        max_length=10,
        null=True,
        blank=True
    )

    email = models.EmailField(
        max_length=50,
        null=True,
        blank=True
    )

    def __str__(self):
        return f'{self.family_name}, {self.familyID}'
    
    def get_absolute_url(self):
        return reverse("family-detail", args=[str(self.familyID)])

class Person(models.Model):
    #Model representing an individual person.

    personID = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        help_text="Unique Person ID for this particular person."
    )

    first_name = models.CharField(
        max_length=20,
        help_text="Enter the person's first name."
    )

    last_name = models.CharField(
        max_length=20,
        help_text="Enter the person's last name."
    )

    associated_family = models.ForeignKey(
        Family,
        help_text="Enter the family last name associated with this person.",
        on_delete=models.RESTRICT,
        null=True,
        related_name='people',
    )

    RSVP_STATUS = (
        ('y', 'Yes'),
        ('n', 'No')
    )

    status = models.CharField(
        max_length=1,
        choices=RSVP_STATUS,
        blank=True,
        default='n',
        help_text="RSVP Status."
    )
    
    class Meta:
        ordering = ['first_name', 'last_name']

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    
    def get_absolute_url(self):
        return reverse("person-detail", args=[str(self.personID)])
    
    



