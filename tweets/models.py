from django.db import models
import random

# Create your models here. maps django to a database 

class Tweet(models.Model):
    # id = modles.AutoField(primary_key=True)
    content = models.TextField(blank=True,null=True)
    image = models.FileField(upload_to='images/',blank=True,null=True)
    # likes = models.IntegerField(blank=True,null=True)

    class Meta:
        ordering = ['-id']

    def serialize(self):
        return {
            "id": self.id,
            "content": self.content,
            'likes': random.randint(0,100),
        }
