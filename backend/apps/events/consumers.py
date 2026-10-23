# events/consumers.py
import json
from django.utils import timezone
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import SupportMessage


class SupportChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = "chat_support_room"
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            message_text = data.get("message", "").strip()

            if not message_text:
                return

            # Save message to database asynchronously
            await self.save_message('user', message_text)

            now = timezone.now()
            payload = {
                "id": int(now.timestamp() * 1000),
                "text": message_text,
                "sender": "user",
                "timestamp": now.strftime("%I:%M %p")
            }

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "chat_message",
                    "message_data": payload
                }
            )
        except Exception as e:
            print(f"Error in WebSocket receive: {e}")

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event["message_data"]))

    @database_sync_to_async
    def save_message(self, sender, text):
        return SupportMessage.objects.create(sender=sender, text=text)