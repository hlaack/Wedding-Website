from datetime import date

from django.test import TestCase
from django.urls import reverse
from django.test import override_settings


class RsvpDeadlineTests(TestCase):
    @override_settings(RSVP_DEADLINE=date(2020, 1, 1), SECURE_SSL_REDIRECT=False)
    def test_closed_deadline_redirects_to_notice_page(self):
        response = self.client.get(reverse('password_entry'))

        self.assertRedirects(response, reverse('rsvp_closed'))
