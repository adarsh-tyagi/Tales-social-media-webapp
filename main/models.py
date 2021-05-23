from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from PIL import Image

# Create your models here.

class Post(models.Model):
    message = models.TextField()
    date = models.DateTimeField(default=datetime.now())
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to="profile_pics/")
    status = models.TextField()

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self):
        super().save()

        img = Image.open(self.image.path)
        # if img.height > 300 or img.width > 300:
        #     output_size = (300, 300)
        #     img.thumbnail(output_size)
        img.save(self.image.path)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    date = models.DateTimeField(default=datetime.now())

class Followers(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    another_user = models.ManyToManyField(User, related_name='another_user')

    def __str__(self) -> str:
        return self.user.username  
