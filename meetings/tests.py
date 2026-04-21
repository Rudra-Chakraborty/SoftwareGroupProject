# Author: Student 4
# Module: Schedule
# Description: Tests for the meetings/schedule module.

from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import date, time
from .models import Meeting


class MeetingModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.meeting = Meeting.objects.create(
            title='Team Standup',
            organiser=self.user,
            team_name='Software 2',
            date=date(2026, 5, 1),
            start_time=time(10, 0),
            end_time=time(10, 30),
            platform='zoom',
            description='Daily standup meeting'
        )

    def test_meeting_str(self):
        """Meeting string representation is correct"""
        self.assertEqual(
            str(self.meeting),
            'Team Standup on 2026-05-01 at 10:00:00'
        )

    def test_meeting_created_successfully(self):
        """Meeting is saved to the database with correct fields"""
        self.assertEqual(Meeting.objects.count(), 1)
        self.assertEqual(self.meeting.title, 'Team Standup')
        self.assertEqual(self.meeting.platform, 'zoom')


class MeetingViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.meeting = Meeting.objects.create(
            title='Team Standup',
            organiser=self.user,
            team_name='Software 2',
            date=date(2026, 5, 1),
            start_time=time(10, 0),
            end_time=time(10, 30),
            platform='zoom',
            description='Daily standup meeting'
        )

    def test_upcoming_view_requires_login(self):
        """Unauthenticated users are redirected to login"""
        response = self.client.get(reverse('schedule:upcoming'))
        self.assertEqual(response.status_code, 302)

    def test_upcoming_view_loads_for_logged_in_user(self):
        """Upcoming page loads successfully for logged in user"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('schedule:upcoming'))
        self.assertEqual(response.status_code, 200)

    def test_create_meeting_get(self):
        """Create meeting form page loads correctly"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('schedule:create'))
        self.assertEqual(response.status_code, 200)

    def test_create_meeting_post(self):
        """A valid form submission creates a new meeting"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('schedule:create'), {
            'title': 'New Meeting',
            'team_name': 'Software 2',
            'date': '2026-06-01',
            'start_time': '14:00',
            'end_time': '15:00',
            'platform': 'teams',
            'meeting_link': '',
            'description': 'Test meeting',
        })
        self.assertEqual(Meeting.objects.count(), 2)

    def test_delete_meeting(self):
        """Organiser can delete their own meeting"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(
            reverse('schedule:delete', args=[self.meeting.pk])
        )
        self.assertEqual(Meeting.objects.count(), 0)

    def test_non_organiser_cannot_delete(self):
        """A different user cannot delete someone else's meeting"""
        other_user = User.objects.create_user(
            username='otheruser',
            password='testpass123'
        )
        self.client.login(username='otheruser', password='testpass123')
        response = self.client.post(
            reverse('schedule:delete', args=[self.meeting.pk])
        )
        self.assertEqual(Meeting.objects.count(), 1)