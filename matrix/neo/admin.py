from django.contrib import admin
from neo.models import UserProfileInfo
from neo.models import FileTransferInfo

# Register your models here.

admin.site.register(UserProfileInfo)
admin.site.register(FileTransferInfo)
