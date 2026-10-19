from channels.db import database_sync_to_async
from channels.testing import WebsocketCommunicator
from django.contrib.auth.models import AnonymousUser, User
from django.test import TestCase, TransactionTestCase
from django.urls import reverse

from chat.models import Message, Room
from config.asgi import application


class ChatConsumerTests(TransactionTestCase):
    def setUp(self):
        self.ali = User.objects.create_user('ali', password='Kuchli_parol_123')
        self.vali = User.objects.create_user('vali', password='Kuchli_parol_123')
        self.room = Room.objects.create(name='Python', slug='python', created_by=self.ali)

    async def connect(self, user, slug='python'):
        communicator = WebsocketCommunicator(
            application, f'/ws/rooms/{slug}/', headers=[(b'origin', b'http://localhost')]
        )
        communicator.scope['user'] = user
        connected, _ = await communicator.connect()
        return communicator, connected

    async def test_message_saved_and_sent(self):
        ali, connected = await self.connect(self.ali)
        self.assertTrue(connected)
        await ali.receive_json_from()
        vali, _ = await self.connect(self.vali)
        await vali.receive_json_from()
        await ali.receive_json_from()

        await ali.send_json_to({'message': 'Salom'})
        data = await vali.receive_json_from()
        self.assertEqual(data['type'], 'message')
        self.assertEqual(data['username'], 'ali')
        self.assertEqual(data['message'], 'Salom')
        count = await database_sync_to_async(Message.objects.filter(room=self.room, user=self.ali).count)()
        self.assertEqual(count, 1)
        await ali.disconnect()
        await vali.disconnect()

    async def test_join_event(self):
        ali, _ = await self.connect(self.ali)
        self.assertEqual(await ali.receive_json_from(), {'type': 'join', 'username': 'ali'})
        await ali.disconnect()

    async def test_anonymous_rejected(self):
        _, connected = await self.connect(AnonymousUser())
        self.assertFalse(connected)

    async def test_unknown_room_rejected(self):
        _, connected = await self.connect(self.ali, slug='yoq')
        self.assertFalse(connected)

    async def test_empty_message_ignored(self):
        ali, _ = await self.connect(self.ali)
        await ali.receive_json_from()
        await ali.send_json_to({'message': '   '})
        self.assertTrue(await ali.receive_nothing())
        await ali.disconnect()


class ChatViewsTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('ali', password='Kuchli_parol_123')

    def test_login_required(self):
        response = self.client.get(reverse('room_list'))
        self.assertEqual(response.status_code, 302)

    def test_create_room(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('room_list'), {'name': 'Django Chat'})
        self.assertRedirects(response, reverse('room_detail', args=['django-chat']))

    def test_duplicate_room(self):
        self.client.force_login(self.user)
        self.client.post(reverse('room_list'), {'name': 'Python'})
        self.client.post(reverse('room_list'), {'name': 'python'})
        self.assertEqual(Room.objects.count(), 1)

    def test_room_shows_history(self):
        room = Room.objects.create(name='Python', slug='python', created_by=self.user)
        Message.objects.create(room=room, user=self.user, text='Eski xabar')
        self.client.force_login(self.user)
        response = self.client.get(reverse('room_detail', args=['python']))
        self.assertContains(response, 'Eski xabar')
