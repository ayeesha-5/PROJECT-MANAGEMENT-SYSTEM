from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from chat.models import ChatRoom, Message
from projects.models import Project


@login_required
def chat_list(request):
    if request.user.role == 'super_admin':
        projects = Project.objects.all()
    elif request.user.role == 'project_manager':
        projects = Project.objects.filter(created_by=request.user)
    else:
        projects = request.user.assigned_projects.all()

    chat_rooms = []
    for project in projects:
        room, created = ChatRoom.objects.get_or_create(project=project)
        chat_rooms.append(room)

    return render(request, 'chat/chat_list.html', {'chat_rooms': chat_rooms})


@login_required
def chat_room(request, room_id):
    room = get_object_or_404(ChatRoom, id=room_id)
    messages_list = Message.objects.filter(room=room).order_by('timestamp')
    return render(request, 'chat/chat_room.html', {
        'room': room,
        'messages_list': messages_list,
        'user': request.user
    })