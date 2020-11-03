from re import T
from tweets.forms import MAX_TWEET_LENGTH
from rest_framework import serializers

from .models import Tweet

from django .conf import settings

MAX_TWEET_LENGTH = settings.MAX_TWEET_LENGTH

class TweetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tweet
        fields = [
            'content',
            'likes',
        ]
    def validate_content(self, value):
        if len(value) > MAX_TWEET_LENGTH:
            raise serializers.ValidationError("This tweet is too long")
        return value
