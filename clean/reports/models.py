from django.db import models


class Department(models.Model):
    name = models.CharField(max_length=200)
    leader = models.CharField(max_length=200, blank=True)
    specialisation = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)

    class Meta:
        managed = False
        db_table = 'teams_department'

    def __str__(self):
        return self.name


class Team(models.Model):
    name = models.CharField(max_length=200)
    manager = models.CharField(max_length=200, blank=True)
    purpose = models.TextField(blank=True)
    responsibilities = models.TextField(blank=True)
    skills = models.CharField(max_length=500, blank=True)
    contact_email = models.EmailField(blank=True)
    repository_url = models.CharField(max_length=200, blank=True)
    contact_channel = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    department = models.ForeignKey(
        Department, on_delete=models.CASCADE,
        db_column='department_id', related_name='teams'
    )

    class Meta:
        managed = False
        db_table = 'teams_team'

    def __str__(self):
        return self.name


class TeamMember(models.Model):
    name = models.CharField(max_length=200)
    role = models.CharField(max_length=200, blank=True)
    email = models.EmailField(blank=True)
    team = models.ForeignKey(
        Team, on_delete=models.CASCADE,
        db_column='team_id', related_name='members'
    )

    class Meta:
        managed = False
        db_table = 'teams_teammember'

    def __str__(self):
        return self.name
