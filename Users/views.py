import http
from .models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.models import User
from rest_framework.exceptions import AuthenticationFailed
import jwt
from gigachat import settings


# Create your views here.

def get_user_from_token(token):
    try:
        decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        user_id = decoded_token['user_id']
        user = User.objects.get(id=user_id)
        return user
    except (jwt.DecodeError, User.DoesNotExist):
        return None


def find_members_chat(user_i, user_j):
    members_i = Member.objects.filter(user=user_i).values('chat')
    members_j = Member.objects.filter(user=user_j).values('chat')
    return members_j.intersection(members_i)


def send_message(text, sender_id, chat_id, reply_to_id=None):
    try:
        sender = UserProfile.objects.get(id=sender_id)
        chat = Chat.objects.get(id=chat_id)
        if reply_to_id is not None:
            reply_message = Message.objects.get(chat=chat, message_id=reply_to_id)
            message = Message.objects.create(chat=chat, text=text, sender=sender, reply_to=reply_message)
        else:
            message = Message.objects.create(chat=chat, text=text, sender=sender)
        return message
    except Exception as error:
        raise ValidationError(f"couldn't send the message ,{error}")


def create_private_chat(sender_id, receiver_id):
    try:
        sender = UserProfile.objects.get(id=sender_id)
        receiver = UserProfile.objects.get(id=receiver_id)
        if find_members_chat(sender, receiver).exists():
            return Response({'status': f"chat created before "}, status=status.HTTP_200_OK)
        chat = Chat.objects.create(isPrivate=True)
        Member.objects.create(chat=chat, user=sender)
        Member.objects.create(chat=chat, user=receiver)
        return chat
    except Exception as error:
        raise ValidationError(f"couldn't make the chat ,{error}")


class RegisterView(APIView):
    def post(self, request):
        try:
            username = request.data['username']
            password = request.data['password']
            description = request.data['description']
            user = User.objects.create(username=username, password=password, is_superuser=False)
            user.save()
            user_profile = UserProfile.objects.create(user=user, description=description)
            user_profile.save()
            return Response(data={'message': "account created"}, status=http.HTTPStatus.CREATED)
        except Exception as error:
            return Response({'error': error}, status=http.HTTPStatus.BAD_REQUEST)
