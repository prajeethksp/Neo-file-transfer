from django.db import models

# we will be using django's existing user models
from django.contrib.auth.models import User


# Create your models here.

class UserProfileInfo(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
    
class FileTransferInfo(models.Model):

    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    sender_name = models.CharField(max_length=255, null=True, blank=True, verbose_name='Sender Name')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
    file_path = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.sender.username} to {self.receiver.username}"
    
from storages.backends.gcloud import GoogleCloudStorage
storage = GoogleCloudStorage()
class UploadToBucket():
    @staticmethod
    def upload_files(file, filename):
        try:
            target_path = '/files/' + filename
            path = storage.save(target_path, file)
            return storage.url(path)
        except Exception as e:
            print(e)

