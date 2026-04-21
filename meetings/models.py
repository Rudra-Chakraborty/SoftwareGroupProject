# Author: Student 4
# Module: Schedule
# Description: Database model for the meeting scheduling feature.
from django.db import models
from django.contrib.auth.models import User
PLATFORM_CHOICES = [
    ('zoom', 'Zoom'),
    ('teams', 'Microsoft Teams'),
    ('slack', 'Slack Huddle'),
    ('google_meet', 'Google Meet'),
    ('in_person', 'In Person'),
]
class Meeting(models.Model):
    title = models.CharField(max_length=200)
    organiser = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='organised_meetings'
    )
    
    # INTEGRATION NOTE: Replace this with a ForeignKey to Student 1's
    # Team model after Friday's group meeting.
    team_name = models.CharField(max_length=100, blank=True, default='')
    
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    
    platform = models.CharField(
        max_length=20,
        choices=PLATFORM_CHOICES,
        default='zoom'
    )
    meeting_link = models.URLField(blank=True, default='')
    
    description = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['date', 'start_time']

    def __str__(self):
        return f"{self.title} on {self.date} at {self.start_time}"