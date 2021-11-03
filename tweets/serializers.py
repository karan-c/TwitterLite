from django.db import models
from django.db.models import fields
from rest_framework import serializers
from twitterlite.settings import MAX_TWEET_LENGTH
from .models import Tweet

class TweetLikeSerializer(serializers.Serializer):
	tweet_id = serializers.IntegerField()
	action = serializers.CharField()
	content = serializers.CharField(allow_blank=True, required=False, max_length=MAX_TWEET_LENGTH)

class TweetDetailSerializer(serializers.ModelSerializer):
	likes = serializers.SerializerMethodField(read_only=True)
	retweet_obj = serializers.SerializerMethodField(read_only=True)
	class Meta:
		model = Tweet
		fields = ['content', 'timestamp', 'id', 'user', 'likes', 'retweet_obj']
	
	def get_likes(self, obj):
		return obj.likes.count()

	def get_retweet_obj(self, obj):
		if obj.retweet_obj != None:
			return TweetDetailSerializer(obj.retweet_obj).data
		else:
			return None

class TweetCreateSerializer(serializers.ModelSerializer):
	likes = serializers.SerializerMethodField(read_only=True)
	class Meta:
		model = Tweet
		fields = ['content', 'timestamp', 'id', 'likes']

	def get_likes(self, obj):
		return obj.likes.count()

	def validate_content(self, value):
		if (len(value) > MAX_TWEET_LENGTH):
			raise serializers.ValidationError("Tweet is longer than max length")
		return value
