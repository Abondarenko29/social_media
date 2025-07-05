import json
from channels.generic.websocket import AsyncWebsocketConsumer


class WebRTCConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        message_type = text_data_json.get('type')
        if message_type == 'offer':
            # Handle offer
            pass
        elif message_type == 'answer':
            # Handle answer
            pass
        elif message_type == 'ice_candidate':
            # Handle ice candidate
            pass

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender_channel_name': self.channel_name
            }
        )

    async def chat_message(self, event):
        message = event['message']
        sender_channel_name = event['sender_channel_name']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender_channel_name == self.channel_name
        }))
