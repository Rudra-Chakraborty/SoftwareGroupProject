from django.db import models

class Department(models.Model):
    name = models.CharField(max_length=200)
    leader = models.CharField(max_length=200, blank=True)
    specialisation = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Team(models.Model):
    name = models.CharField(max_length=200)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='teams')
    manager = models.CharField(max_length=200, blank=True)
    purpose = models.TextField(blank=True)
    responsibilities = models.TextField(blank=True)
    skills = models.CharField(max_length=500, blank=True)
    contact_email = models.EmailField(blank=True)
    repository_url = models.URLField(blank=True)
    contact_channel = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)
    upstream_dependencies = models.ManyToManyField(
        'self',
        blank=True,
        symmetrical=False,
        related_name='downstream_dependencies'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['department__name', 'name']

    def __str__(self):
        return self.name


class TeamMember(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='members')
    name = models.CharField(max_length=200)
    role = models.CharField(max_length=200, blank=True)
    email = models.EmailField(blank=True)

    class Meta:
        ordering = ['team__name', 'name']

    def __str__(self):
        return f'{self.name} ({self.team.name})'


class TeamMessage(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='messages')
    sender_name = models.CharField(max_length=200)
    sender_email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.subject} -> {self.team.name}'


class TeamMeeting(models.Model):
    PLATFORM_CHOICES = [
        ('teams', 'Microsoft Teams'),
        ('zoom', 'Zoom'),
        ('slack', 'Slack'),
        ('google_meet', 'Google Meet'),
        ('in_person', 'In Person'),
    ]

    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='meetings')
    organiser = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='team_meetings')
    title = models.CharField(max_length=200)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    platform = models.CharField(max_length=30, choices=PLATFORM_CHOICES)
    meeting_link = models.URLField(blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['date', 'start_time']

    def __str__(self):
        return f'{self.title} - {self.team.name}'
