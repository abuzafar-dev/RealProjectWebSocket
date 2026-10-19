from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class AccountsTests(TestCase):
    def test_register(self):
        response = self.client.post(reverse('register'), {
            'username': 'ali',
            'email': 'ali@example.com',
            'first_name': 'Ali',
            'password1': 'Kuchli_parol_123',
            'password2': 'Kuchli_parol_123',
        })
        self.assertRedirects(response, reverse('room_list'))
        self.assertTrue(User.objects.filter(username='ali').exists())

    def test_login(self):
        User.objects.create_user('vali', password='Kuchli_parol_123')
        response = self.client.post(reverse('login'), {'username': 'vali', 'password': 'Kuchli_parol_123'})
        self.assertRedirects(response, reverse('room_list'))

    def test_logout(self):
        user = User.objects.create_user('vali', password='Kuchli_parol_123')
        self.client.force_login(user)
        self.client.post(reverse('logout'))
        response = self.client.get(reverse('room_list'))
        self.assertEqual(response.status_code, 302)
