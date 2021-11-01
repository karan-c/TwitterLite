from django.db import models
from rest_framework import serializers
from twitterlite.settings import MAX_TWEET_LENGTH
from .models import Tweet

class TweetLikeSerializer(serializers.Serializer):
    tweet_id = serializers.IntegerField()
    action = serializers.CharField()

class TweetSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField()
    class Meta:
        model = Tweet
        fields = ['content', 'timestamp', 'id', 'likes']

    def get_likes(self, obj):
        return obj.likes.count()

    def validate_content(self, value):
        if (len(value) > MAX_TWEET_LENGTH):
            raise serializers.ValidationError("Tweet is longer than max length")
        return value
