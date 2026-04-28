from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]
    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('leader', models.CharField(blank=True, max_length=200)),
                ('specialisation', models.CharField(blank=True, max_length=255)),
                ('description', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('manager', models.CharField(blank=True, max_length=200)),
                ('purpose', models.TextField(blank=True)),
                ('responsibilities', models.TextField(blank=True)),
                ('skills', models.CharField(blank=True, max_length=500)),
                ('contact_email', models.EmailField(blank=True, max_length=254)),
                ('repository_url', models.URLField(blank=True)),
                ('contact_channel', models.CharField(blank=True, max_length=255)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='teams', to='teams.department')),
            ],
            options={'ordering': ['department__name', 'name']},
        ),
        migrations.CreateModel(
            name='TeamMember',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('role', models.CharField(blank=True, max_length=200)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='members', to='teams.team')),
            ],
            options={'ordering': ['team__name', 'name']},
        ),
        migrations.CreateModel(
            name='TeamMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sender_name', models.CharField(max_length=200)),
                ('sender_email', models.EmailField(max_length=254)),
                ('subject', models.CharField(max_length=200)),
                ('message', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='teams.team')),
            ],
            options={'ordering': ['-created_at']},
        ),
        migrations.CreateModel(
            name='TeamMeeting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('date', models.DateField()),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('platform', models.CharField(choices=[('teams', 'Microsoft Teams'), ('zoom', 'Zoom'), ('slack', 'Slack'), ('google_meet', 'Google Meet'), ('in_person', 'In Person')], max_length=30)),
                ('meeting_link', models.URLField(blank=True)),
                ('description', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('organiser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='team_meetings', to=settings.AUTH_USER_MODEL)),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='meetings', to='teams.team')),
            ],
            options={'ordering': ['date', 'start_time']},
        ),
        migrations.AddField(
            model_name='team',
            name='upstream_dependencies',
            field=models.ManyToManyField(blank=True, related_name='downstream_dependencies', to='teams.team'),
        ),
    ]
