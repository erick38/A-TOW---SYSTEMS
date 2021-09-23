from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import About, Category, Clock_in, Gallery, Home, Mensaje, MyUser, Skills
# Register your models here.

admin.site.register(MyUser, UserAdmin)
admin.site.register(Clock_in)
admin.site.register(Gallery)
admin.site.register(Mensaje)
admin.site.register(Category)
admin.site.register(About)
admin.site.register(Home)
admin.site.register(Skills)