from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import get_user_model


# Create your models here.me

class MyUser(AbstractUser):
    username = models.CharField(max_length=30, unique=True)
    created_at = models.DateTimeField(default=timezone.now)

class Session(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    session_key = models.CharField(max_length=40)
    created_at = models.DateTimeField(auto_now_add=True)

class Clock_in(models.Model):
    author = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    STATUS_CHOICES = (
        ('clock-in', 'Clock-in'),
        ('clock-out', 'Clock-out'),
    )
    clock_status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='clock-in', null=False)
    clock_time = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return self.clock_status

    
class Conversation(models.Model):
    participants = models.ManyToManyField(MyUser, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)

class Message(models.Model):
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name='messages',
        verbose_name='Conversation',
        null=False
    )
    sender = models.ForeignKey(
        MyUser,
        on_delete=models.CASCADE,
        related_name='sent_messages',
        verbose_name='Sender',
        null=False
    )
    message = models.TextField(blank=False, verbose_name='Message')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='Created At')