from django.urls import re_path


websocket_urlpatterns=[
    re_path(r'ws/chat/(?p<room_name>\w+)/$',consumers.chatRoomConsumers),
    
]