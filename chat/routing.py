from django.urls import re_path

from chat.consumers import ChatConsumer

websocket_urlpatterns = [
    re_path(r'^ws/rooms/(?P<slug>[-\w]+)/$', ChatConsumer.as_asgi()),
]
