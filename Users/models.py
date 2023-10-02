from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User


def image_validate_file_extension(value):
    import os
    from django.core.exceptions import ValidationError
    ext = os.path.splitext(value.name)[1]
    valid_extension = ['.jpg', '.png']
    if not ext.lower() in valid_extension:
        raise ValidationError('Unsupported file extension')


def media_validate_file_extension(value):
    import os
    from django.core.exceptions import ValidationError
    ext = os.path.splitext(value.name)[1]
    valid_extension = ['.jpg', '.png', 'mp4']
    if not ext.lower() in valid_extension:
        raise ValidationError('Unsupported file extension')


# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.FileField(upload_to='files/user_avatar/', null=True, blank=True,
                              validators=[image_validate_file_extension])
    description = models.CharField(max_length=512, null=False, blank=False)

    def __str__(self):
        return self.user.username


class Chat(models.Model):
    isPrivate = models.BooleanField(null=False, blank=False)


class Member(models.Model):
    chat = models.ForeignKey('Chat', on_delete=models.CASCADE, related_name="members")
    user = models.ForeignKey('UserProfile', on_delete=models.DO_NOTHING, related_name="chats")

    def clean(self):
        if self.chat.isPrivate and self.chat.members.count() > 1:
            raise ValidationError("Private chats can't have more than two members.")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['chat', 'user'], name="unique_member")
        ]


class Message(models.Model):
    chat = models.ForeignKey('Chat', on_delete=models.CASCADE, related_name="messages")
    text = models.CharField(max_length=2048, null=False, blank=False)
    file = models.FileField(upload_to='files/documents', null=True, blank=True)
    sender = models.ForeignKey('UserProfile', on_delete=models.DO_NOTHING, null=True)
    reply_to = models.ForeignKey('Message', on_delete=models.DO_NOTHING, null=True, blank=True)
    message_id = models.IntegerField(blank=True, null=True)

    def clean(self):
        self.message_id = self.chat.messages.count() + 1
        if self.sender.id not in [x['user_id'] for x in list(self.chat.members.values("user_id"))]:
            raise ValidationError("error occurred! chat not found")
        if self.reply_to is not None:
            if self.reply_to.chat.id != self.chat.id:
                raise ValidationError("error occurred! message not found")
