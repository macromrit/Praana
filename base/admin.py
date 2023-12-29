from django.contrib import admin

# Register your models here.
# this one's used to display and manipulate tables made in db
# on admin panel. show it.

from .models import Room, Topic, Message, User, Article

admin.site.register(Room)
admin.site.register(Topic)
admin.site.register(Message)
admin.site.register(User)
admin.site.register(Article)