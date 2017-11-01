from django.contrib import admin
from .models import *
from django.contrib.auth.models import User
# Register your models here.

admin.site.register(UserProfile)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Comment)
admin.site.register(Vote)
admin.site.register(Notification)
admin.site.register(Tag)
admin.site.register(Topic)
admin.site.register(Message)
admin.site.register(Follow)
