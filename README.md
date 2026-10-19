# RealProjectWebSocket — Real-time Chat

Django Channels asosidagi real-time chat. Foydalanuvchilar ro'yxatdan o'tib, xonalar yaratadi va bir-biri bilan jonli yozishadi. Xabarlar bazada saqlanadi.

## Imkoniyatlar

- Ro'yxatdan o'tish, kirish, chiqish
- Xona yaratish (nomidan avtomatik slug yasaladi, takrorlanmaydi)
- WebSocket orqali jonli xabarlar
- Xabarlar bazaga yoziladi, xonaga kirganda oxirgi 50 ta xabar ko'rinadi
- "... xonaga kirdi / chiqdi" xabarlari
- Faqat tizimga kirgan foydalanuvchi WebSocket'ga ulana oladi
- Origin tekshiruvi (`AllowedHostsOriginValidator`)

## Ishga tushirish

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py runserver
```

http://127.0.0.1:8000/ — ikki xil brauzerda (yoki bittasini incognito'da) ikki foydalanuvchi bilan kiring va bitta xonada yozishib ko'ring.

## Tuzilishi

```
accounts/            ro'yxatdan o'tish, login
chat/
  models.py          Room, Message
  consumers.py       ChatConsumer (connect, receive, disconnect)
  routing.py         ws/rooms/<slug>/
  views.py           xonalar ro'yxati, xona sahifasi
config/asgi.py       http + websocket routing
```

Production uchun `CHANNEL_LAYERS` ni `channels_redis` ga almashtirish kerak.

## Testlar

```bash
python manage.py test
```
