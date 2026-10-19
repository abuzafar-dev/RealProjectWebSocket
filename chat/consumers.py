import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.utils import timezone

from chat.models import Message, Room


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        if not self.user.is_authenticated:
            await self.close()
            return
        self.room = await self.get_room(self.scope['url_route']['kwargs']['slug'])
        if self.room is None:
            await self.close()
            return
        self.group_name = f'room_{self.room.id}'
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()
        await self.channel_layer.group_send(
            self.group_name,
            {'type': 'chat.event', 'event': 'join', 'username': self.user.username},
        )

    async def disconnect(self, close_code):
        if hasattr(self, 'group_name'):
            await self.channel_layer.group_send(
                self.group_name,
                {'type': 'chat.event', 'event': 'leave', 'username': self.user.username},
            )
            await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
        except json.JSONDecodeError:
            return
        text = str(data.get('message', '')).strip()[:1000]
        if not text:
            return
        message = await self.save_message(text)
        await self.channel_layer.group_send(self.group_name, {
            'type': 'chat.message',
            'message': text,
            'username': self.user.username,
            'time': timezone.localtime(message.created_at).strftime('%H:%M'),
        })

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'type': 'message',
            'message': event['message'],
            'username': event['username'],
            'time': event['time'],
        }))

    async def chat_event(self, event):
        await self.send(text_data=json.dumps({
            'type': event['event'],
            'username': event['username'],
        }))

    @database_sync_to_async
    def get_room(self, slug):
        return Room.objects.filter(slug=slug).first()

    @database_sync_to_async
    def save_message(self, text):
        return Message.objects.create(room=self.room, user=self.user, text=text)
