from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Chat)
admin.site.register(Member)
admin.site.register(Message)