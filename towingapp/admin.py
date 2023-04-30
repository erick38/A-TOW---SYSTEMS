from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Clock_in, Message, MyUser, Session,Conversation, ReceiptPart1,ReceiptPart2,ReceiptPart3, ReceiptPart4
# Register your models here.

admin.site.register(MyUser, UserAdmin)
admin.site.register(Clock_in)
admin.site.register(Message)
admin.site.register(Session)
admin.site.register(Conversation)
admin.site.register(ReceiptPart1)
admin.site.register(ReceiptPart2)
admin.site.register(ReceiptPart3)
admin.site.register(ReceiptPart4)