from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render

from chat.forms import RoomForm
from chat.models import Room


@login_required
def room_list(request):
    form = RoomForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        room = form.save(commit=False)
        room.created_by = request.user
        room.save()
        return redirect(room)
    rooms = Room.objects.annotate(message_count=Count('messages')).order_by('name')
    return render(request, 'chat/room_list.html', {'rooms': rooms, 'form': form})


@login_required
def room_detail(request, slug):
    room = get_object_or_404(Room, slug=slug)
    chat_messages = room.messages.select_related('user').order_by('-created_at')[:50]
    return render(request, 'chat/room_detail.html', {'room': room, 'chat_messages': reversed(chat_messages)})
