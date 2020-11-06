from django.db import models
from django.conf import settings
import random

# Create your models here. maps django to a database 

User = settings.AUTH_USER_MODEL

class TweetLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    tweet = models.ForeignKey("Tweet", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

class Tweet(models.Model):
    # id = modles.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  #many users have many tweets tweet only has one user, cascade: owner user deleted, all tweets deleted.
    content = models.TextField(blank=True,null=True)
    image = models.FileField(upload_to='images/',blank=True,null=True)
    likes = models.ManyToManyField(User, related_name='tweet_user', blank=True, through=TweetLike)
    timestamp = models.DateTimeField(auto_now_add=True)


    # likes = models.IntegerField(blank=True,null=True)

    def __str__(self):
        return self.content

    class Meta:
        ordering = ['-id']

    def serialize(self):
        return {
            "id": self.id,
            "content": self.content,
            # 'likes': random.randint(0,100),
            "likes" : self.likes
        }
