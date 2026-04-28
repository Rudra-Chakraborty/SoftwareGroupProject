# Author: Student 4
# Module: Schedule
# Description: Views for monthly calendar, weekly view, upcoming meetings,
# and create/edit/delete operations on meetings.

import calendar
from datetime import date, timedelta

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import MeetingForm
from .models import Meeting
@login_required
def upcoming_view(request):
    today = timezone.now().date()
    meetings = Meeting.objects.filter(date__gte=today).order_by('date', 'start_time')
    return render(request, 'meetings/upcoming.html', {
        'meetings': meetings,
        'today': today,
    })
@login_required
def monthly_view(request):
    today = timezone.now().date()
    year = int(request.GET.get('year', today.year))
    month = int(request.GET.get('month', today.month))

    if month < 1:
        month = 12
        year -= 1
    elif month > 12:
        month = 1
        year += 1

    cal = calendar.Calendar(firstweekday=0)
    weeks = cal.monthdatescalendar(year, month)
    all_dates = [d for week in weeks for d in week]
    meetings = Meeting.objects.filter(date__in=all_dates)

    meetings_by_date = {}
    for meeting in meetings:
        meetings_by_date.setdefault(meeting.date, []).append(meeting)

    first_of_month = date(year, month, 1)
    prev_month_date = (first_of_month - timedelta(days=1))
    next_month_date = (first_of_month + timedelta(days=32)).replace(day=1)

    context = {
        'weeks': weeks,
        'meetings_by_date': meetings_by_date,
        'year': year,
        'month': month,
        'month_name': calendar.month_name[month],
        'today': today,
        'prev_year': prev_month_date.year,
        'prev_month': prev_month_date.month,
        'next_year': next_month_date.year,
        'next_month': next_month_date.month,
        'day_names': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
    }
    return render(request, 'meetings/monthly.html', context)

    
@login_required
def weekly_view(request):
    today = timezone.now().date()

    start_str = request.GET.get('start')
    if start_str:
        try:
            from datetime import datetime
            week_start = datetime.strptime(start_str, '%Y-%m-%d').date()
        except ValueError:
            week_start = today - timedelta(days=today.weekday())
    else:
        week_start = today - timedelta(days=today.weekday())

    week_dates = [week_start + timedelta(days=i) for i in range(7)]
    meetings = Meeting.objects.filter(date__in=week_dates)

    meetings_by_date = {}
    for meeting in meetings:
        meetings_by_date.setdefault(meeting.date, []).append(meeting)

    prev_week = week_start - timedelta(days=7)
    next_week = week_start + timedelta(days=7)

    context = {
        'week_dates': week_dates,
        'meetings_by_date': meetings_by_date,
        'today': today,
        'prev_week': prev_week,
        'next_week': next_week,
        'week_start': week_start,
        'week_end': week_dates[-1],
    }
    return render(request, 'meetings/weekly.html', context)
@login_required
def create_meeting(request):
    if request.method == 'POST':
        form = MeetingForm(request.POST)
        if form.is_valid():
            meeting = form.save(commit=False)
            meeting.organiser = request.user
            meeting.save()
            messages.success(request, 'Meeting scheduled successfully.')
            return redirect('schedule:upcoming')
    else:
        form = MeetingForm()
    return render(request, 'meetings/meeting_form.html', {
        'form': form,
        'action': 'Schedule',
    })
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
            messages.success(request, 'Meeting updated.')
            return redirect('schedule:upcoming')
    else:
        form = MeetingForm(instance=meeting)

    return render(request, 'meetings/meeting_form.html', {
        'form': form,
        'action': 'Update',
        'meeting': meeting,
    })


@login_required
def delete_meeting(request, pk):
    meeting = get_object_or_404(Meeting, pk=pk)
    if meeting.organiser != request.user:
        messages.error(request, 'You can only delete meetings you organised.')
        return redirect('schedule:upcoming')

    if request.method == 'POST':
        meeting.delete()
        messages.success(request, 'Meeting deleted.')
        return redirect('schedule:upcoming')

    return render(request, 'meetings/confirm_delete.html', {'meeting': meeting})

@login_required
def meeting_detail(request, pk):
    meeting = get_object_or_404(Meeting, pk=pk)
    return render(request, 'meetings/meeting_detail.html', {'meeting': meeting})
