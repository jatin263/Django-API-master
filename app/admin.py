from django.contrib import admin
from .models import adminWeb, studentData,user,voiceRecData

# Register your models here.
admin.site.register(user)
admin.site.register(adminWeb)
admin.site.register(studentData)
admin.site.register(voiceRecData)
