from channels.generic.websocket import AsyncWebsocketConsumer
import json
from datetime import datetime
import asyncio

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken
from .models import UserProfile, Chat, Member
from django.contrib.auth.models import User
import jwt
from gigachat import settings


def can_access_chat(user, chat_id):
    userprofile = UserProfile.objects.get(user=user)
    chat = Chat.objects.get(id=chat_id)
    member = Member.objects.get(user=userprofile, chat=chat)
    if member is not None:
        return True
    return False


def get_user_from_token(token):
    try:
        decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        user_id = decoded_token['user_id']
        user = User.objects.get(id=user_id)
        return user
    except (jwt.DecodeError, User.DoesNotExist):
        return None


class ChatRoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        self.is_admin = False
        token = self.scope['url_route']['kwargs']['token']
        if token != "" or token is not None:
            if token == settings.SECRET_KEY:
                self.is_admin = True
                await self.accept()
        else:
            user = get_user_from_token(token)
            if user is not None:
                if can_access_chat(user, self.room_name):
                    await self.channel_layer.group_add(
                        self.room_group_name,
                        self.channel_name
                    )
                    await self.accept()
                else:
                    await self.close()
            else:
                await self.close()

    async def receive(self, text_data):
        pass

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def send_message(self, event):
        message = event['message']
        username = event['username']

        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
        }))

