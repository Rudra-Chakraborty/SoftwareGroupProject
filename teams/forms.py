from django import forms
from .models import TeamMessage, TeamMeeting

class TeamMessageForm(forms.ModelForm):
    class Meta:
        model = TeamMessage
        fields = ['sender_name', 'sender_email', 'subject', 'message']
        widgets = {
            'sender_name': forms.TextInput(attrs={'class': 'form-control'}),
            'sender_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }


class TeamMeetingForm(forms.ModelForm):
    class Meta:
        model = TeamMeeting
        fields = ['title', 'date', 'start_time', 'end_time', 'platform', 'meeting_link', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'platform': forms.Select(attrs={'class': 'form-select'}),
            'meeting_link': forms.URLInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

    def clean(self):
        cleaned = super().clean()
        start = cleaned.get('start_time')
        end = cleaned.get('end_time')
        if start and end and end <= start:
            raise forms.ValidationError('End time must be after start time.')
        return cleaned
