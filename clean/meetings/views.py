# Author: Student 4
#Views for the unified schedule page with modal create/edit/delete.

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import MeetingForm
from .models import Meeting


def _get_teams():
    """Return Team objects if the teams app is available, else empty list."""
    try:
        from teams.models import Team
        return Team.objects.all().order_by('name')
    except Exception:
        return []


@login_required
def upcoming_view(request):
    today = timezone.now().date()
    all_meetings = Meeting.objects.select_related('organiser').order_by('date', 'start_time')
    teams = _get_teams()

    context = {
        'all_meetings': all_meetings,
        'today': today,
        'teams': teams,
    }


    if request.session.pop('form_errors', None):
        form_data = request.session.pop('form_data', {})
        form = MeetingForm(form_data)
        form.is_valid()
        context['form_errors'] = form.errors.as_data()
        nfe = form.non_field_errors()
        if nfe:
            context['nfe'] = str(nfe[0])

    return render(request, 'meetings/upcoming.html', context)


@login_required
def create_meeting(request):
    if request.method == 'POST':
        form = MeetingForm(request.POST)
        if form.is_valid():
            meeting = form.save(commit=False)
            meeting.organiser = request.user
            meeting.save()
            messages.success(request, f'"{meeting.title}" scheduled.')
            return redirect('schedule:upcoming')
        request.session['form_errors'] = True
        request.session['form_data'] = request.POST.dict()
    return redirect('schedule:upcoming')


@login_required
def edit_meeting(request, pk):
    meeting = get_object_or_404(Meeting, pk=pk)
    if meeting.organiser != request.user:
        messages.error(request, 'You can only edit meetings you organised.')
        return redirect('schedule:upcoming')

    if request.method == 'POST':
        form = MeetingForm(request.POST, instance=meeting)
        if form.is_valid():
            form.save()
            messages.success(request, f'"{meeting.title}" updated.')
        else:
            messages.error(request, 'Please check the form fields and try again.')
    return redirect('schedule:upcoming')


@login_required
def delete_meeting(request, pk):
    meeting = get_object_or_404(Meeting, pk=pk)
    if meeting.organiser != request.user:
        messages.error(request, 'You can only delete meetings you organised.')
        return redirect('schedule:upcoming')

    if request.method == 'POST':
        title = meeting.title
        meeting.delete()
        messages.success(request, f'"{title}" deleted.')
    return redirect('schedule:upcoming')


@login_required
def meeting_detail(request, pk):
    meeting = get_object_or_404(Meeting, pk=pk)
    return render(request, 'meetings/meeting_detail.html', {'meeting': meeting})



@login_required
def monthly_view(request):
    return redirect('schedule:upcoming')

@login_required
def weekly_view(request):
    return redirect('schedule:upcoming')
