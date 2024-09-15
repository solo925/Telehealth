from django.urls import re_path

from . consumers import ChatRoomConsumer


websocket_urlpatterns=[
    re_path(r'ws/chat/(?p<room_name>\w+)/$',consumers.ChatRoomConsumer),
    
]