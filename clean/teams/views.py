from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

def _group_login_required(request):
    return (
        bool(request.session.get("user_email")) or
        bool(request.session.get("user_id")) or
        getattr(request.user, "is_authenticated", False)
    )


def _staff_context(request):
    staff = None
    try:
        from main.models import Staff, User
        email = request.session.get("user_email")
        user_id = request.session.get("user_id")

        if email:
            group_user = User.objects.filter(email=email).first()
            if group_user:
                staff = Staff.objects.filter(user=group_user).first()

        if staff is None and user_id:
            staff = Staff.objects.filter(user_id=user_id).first()
    except Exception:
        staff = None
    return staff


from .forms import TeamMessageForm, TeamMeetingForm
from .models import Department, Team, TeamMeeting



def dashboard(request):
    if not _group_login_required(request):
        return redirect('login')
    staff = _staff_context(request)
    departments = Department.objects.annotate(team_count=Count('teams'))
    return render(request, 'teams/dashboard.html', {
        'total_teams': Team.objects.count(),
        'total_departments': Department.objects.count(),
        'departments': departments,
        'upcoming_meetings': TeamMeeting.objects.select_related('team', 'organiser').filter(
            date__gte=timezone.localdate()
        )[:5],
        'staff': staff,
    })


def team_list(request):
    if not _group_login_required(request):
        return redirect('login')
    staff = _staff_context(request)
    query = request.GET.get('q', '').strip()
    view_mode = request.GET.get('view', 'grid')

    teams = Team.objects.select_related('department').prefetch_related(
        'members', 'upstream_dependencies', 'downstream_dependencies'
    ).annotate(member_count=Count('members'))

    if query:
        teams = teams.filter(
            Q(name__icontains=query) |
            Q(manager__icontains=query) |
            Q(department__name__icontains=query) |
            Q(skills__icontains=query) |
            Q(purpose__icontains=query) |
            Q(contact_channel__icontains=query)
        )

    context = {
        'teams': teams,
        'query': query,
        'view_mode': view_mode,
        'total_teams': Team.objects.count(),
        'total_departments': Department.objects.count(),
    }
    return render(request, 'teams/team_list.html', context)


def team_detail(request, pk):
    if not _group_login_required(request):
        return redirect('login')
    staff = _staff_context(request)
    team = get_object_or_404(
        Team.objects.select_related('department').prefetch_related(
            'members', 'upstream_dependencies', 'downstream_dependencies', 'meetings'
        ),
        pk=pk
    )
    upcoming_meetings = team.meetings.filter(date__gte=timezone.localdate())[:5]
    return render(request, 'teams/team_detail.html', {
        'team': team,
        'upcoming_meetings': upcoming_meetings,
    })


def email_team(request, pk):
    if not _group_login_required(request):
        return redirect('login')
    staff = _staff_context(request)
    team = get_object_or_404(Team, pk=pk)

    if request.method == 'POST':
        form = TeamMessageForm(request.POST)
        if form.is_valid():
            team_message = form.save(commit=False)
            team_message.team = team
            team_message.save()
            messages.success(request, f'Message saved for {team.name}.')
            return redirect('teams:detail', pk=team.pk)
    else:
        form = TeamMessageForm(initial={
            'sender_name': request.user.get_full_name() or request.user.username,
            'sender_email': request.user.email,
            'subject': f'Contact request for {team.name}',
        })

    return render(request, 'teams/email_team.html', {'team': team, 'form': form})


def schedule_team_meeting(request, pk):
    if not _group_login_required(request):
        return redirect('login')
    staff = _staff_context(request)
    team = get_object_or_404(Team, pk=pk)

    if request.method == 'POST':
        form = TeamMeetingForm(request.POST)
        if form.is_valid():
            meeting = form.save(commit=False)
            meeting.team = team
            meeting.organiser = request.user
            meeting.save()
            messages.success(request, f'Meeting scheduled with {team.name}.')
            return redirect('teams:detail', pk=team.pk)
    else:
        form = TeamMeetingForm(initial={'title': f'Meeting with {team.name}'})

    return render(request, 'teams/schedule_team_meeting.html', {'team': team, 'form': form})


def my_team_meetings(request):
    if not _group_login_required(request):
        return redirect('login')
    staff = _staff_context(request)
    meetings = TeamMeeting.objects.select_related('team', 'organiser').filter(date__gte=timezone.localdate())
    return render(request, 'teams/team_meetings.html', {'meetings': meetings})


def department_list(request):
    if not _group_login_required(request):
        return redirect('login')
    staff = _staff_context(request)
    query = request.GET.get('q', '').strip()

    departments = Department.objects.prefetch_related(
        'teams',
        'teams__members'
    ).annotate(team_count=Count('teams'))

    if query:
        departments = departments.filter(
            Q(name__icontains=query) |
            Q(leader__icontains=query) |
            Q(specialisation__icontains=query) |
            Q(description__icontains=query)
        )

    return render(request, 'teams/department_list.html', {
        'departments': departments,
        'query': query,
        'total_departments': Department.objects.count(),
        'total_teams': Team.objects.count(),
    })


def department_detail(request, pk):
    if not _group_login_required(request):
        return redirect('login')
    staff = _staff_context(request)
    department = get_object_or_404(
        Department.objects.prefetch_related(
            'teams',
            'teams__members',
            'teams__upstream_dependencies',
            'teams__downstream_dependencies'
        ),
        pk=pk
    )

    return render(request, 'teams/department_detail.html', {
        'department': department,
        'teams': department.teams.all(),
    })


def profile(request):
    return render(request, 'teams/profile.html', {
        'staff': staff,
    })


def dependency_list(request):
    if not _group_login_required(request):
        return redirect('login')
    staff = _staff_context(request)
    query = request.GET.get('q', '').strip()
    teams = Team.objects.select_related('department').prefetch_related(
        'upstream_dependencies',
        'downstream_dependencies',
        'members'
    )

    if query:
        teams = teams.filter(
            Q(name__icontains=query) |
            Q(manager__icontains=query) |
            Q(department__name__icontains=query) |
            Q(upstream_dependencies__name__icontains=query) |
            Q(downstream_dependencies__name__icontains=query)
        ).distinct()

    return render(request, 'teams/dependencies.html', {
        'teams': teams,
        'query': query,
        'staff': staff,
    })
