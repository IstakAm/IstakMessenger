from django.urls import path
from . import views

urlpatterns = [
    path('send_message/', views.SendMessage.as_view(), name="send_message"),
    path('create_private_chat/', views.CreatePrivateChat.as_view(), name="create_private_chat"),
]