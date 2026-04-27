# User registration view.

from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, render


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('schedule:upcoming')
    else:
        form = UserCreationForm()
    for field in form.fields.values():
        field.widget.attrs['class'] = 'form-control'
    return render(request, 'registration/register.html', {'form': form})