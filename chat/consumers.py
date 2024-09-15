from channels.generic.websocket import AsyncWebsocketConsumer
from . import consumers

class ChatRoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name= self.scope['url_route']['kwargs']['room_name']
        await(
            
        )