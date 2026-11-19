import json
from datetime import datetime

from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer
from django.shortcuts import redirect, render
from django.utils import timezone

from ..models import SupportMessage


def support(request):
    if request.method == 'POST':
        agent_text = request.POST.get('message', '').strip()

        if agent_text:
            # 1. Save agent message to Database
            SupportMessage.objects.create(sender='agent', text=agent_text)

            # 2. Push message to WebSocket group
            channel_layer = get_channel_layer()
            payload = {
                "id": int(datetime.now().timestamp() * 1000),
                "text": agent_text,
                "sender": "agent",
                "timestamp": datetime.now().strftime("%I:%M %p")
            }

            async_to_sync(channel_layer.group_send)(
                "chat_support_room",
                {
                    "type": "chat_message",
                    "message_data": payload
                }
            )

        return redirect(request.path)

    # Load message history ordered chronologically
    messages = SupportMessage.objects.order_by('created_at')
    return render(request, "events/pages/support.html", {'messages': messages})


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
