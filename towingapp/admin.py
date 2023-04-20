from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Clock_in, Message, MyUser, Session,Conversation
# Register your models here.

admin.site.register(MyUser, UserAdmin)
admin.site.register(Clock_in)
admin.site.register(Message)
admin.site.register(Session)
admin.site.register(Conversation)
