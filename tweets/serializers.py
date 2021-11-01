from django.db import models
from rest_framework import serializers
from twitterlite.settings import MAX_TWEET_LENGTH
from .models import Tweet

class TweetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tweet
        fields = ['content', 'timestamp', 'id']

    def validate_content(self, value):
        if (len(value) > MAX_TWEET_LENGTH):
            raise serializers.ValidationError("Tweet is longer than max length")
        return value
