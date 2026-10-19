from django.contrib.auth import login
from django.shortcuts import redirect, render

from accounts.forms import RegisterForm


def register(request):
    if request.user.is_authenticated:
        return redirect('room_list')
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        login(request, user)
        return redirect('room_list')
    return render(request, 'accounts/register.html', {'form': form})
