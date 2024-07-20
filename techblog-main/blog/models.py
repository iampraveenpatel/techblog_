from django.db import models
from datetime import datetime    
from django.contrib.auth.models import User

# Create your models here.
class Blog(models.Model):
    title = models.CharField(max_length=200)
    cont = models.TextField()
    author = models.CharField(max_length=200)
    created_at = models.DateTimeField(default=datetime.now(), blank=True)
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'
def user_directory_path(instance, filename):
    # File will be uploaded to MEDIA_ROOT/user_<id>/profile/<filename>
    return f'user_{instance.user.id}/profile/{filename}'