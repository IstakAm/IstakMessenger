from django.shortcuts import render
from .models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


# Create your views here.


def find_members_chat(user_i, user_j):
    members_i = Member.objects.filter(user=user_i).values('chat')
    members_j = Member.objects.filter(user=user_j).values('chat')
    return members_j.intersection(members_i)


class SendMessage(APIView):
    def post(self, request, format=None):
        try:
            text = request.GET['text']
            sender_id = request.GET['sender_id']
            sender = UserProfile.objects.get(id=sender_id)
            chat_id = request.GET['chat_id']
            chat = Chat.objects.get(id=chat_id)
            if 'reply_to' in request.GET:
                reply_to_id = request.GET['reply_to']
                reply_message = Message.objects.get(chat=chat, message_id=reply_to_id)
                Message.objects.create(chat=chat, text=text, sender=sender, reply_to=reply_message)
            else:
                Message.objects.create(chat=chat, text=text, sender=sender)
            return Response({'status': "message sent"}, status=status.HTTP_200_OK)
        except Exception as error:
            print(error)
            return Response({'status': "Internal server error , We'll check it later"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CreatePrivateChat(APIView):
    def post(self, request, format=None):
        try:
            sender_id = request.GET['sender_id']
            receiver_id = request.GET['receiver_id']
            sender = UserProfile.objects.get(id=sender_id)
            receiver = UserProfile.objects.get(id=receiver_id)
            if find_members_chat(sender, receiver).exists():
                return Response({'status': f"chat created before "}, status=status.HTTP_200_OK)
            chat = Chat.objects.create(isPrivate=True)
            Member.objects.create(chat=chat, user=sender)
            Member.objects.create(chat=chat, user=receiver)
            return Response({'status': f"chat created chat_id : {chat.id}"}, status=status.HTTP_200_OK)
        except Exception as error:
            print(error)
            return Response({'status': "Internal server error , We'll check it later"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
