from rest_framework import serializers
from twitterlite.settings import MAX_TWEET_LENGTH
from users.models import User
from users.serializers import UserSerializer
from .models import Tweet

class TweetLikeSerializer(serializers.Serializer):
	tweet_id = serializers.IntegerField()
	action = serializers.CharField()
	content = serializers.CharField(allow_blank=True, required=False, max_length=MAX_TWEET_LENGTH)

class TweetDetailSerializer(serializers.ModelSerializer):
	likes = serializers.SerializerMethodField(read_only=True)
	retweet_obj = serializers.SerializerMethodField(read_only=True)
	user = serializers.SerializerMethodField(read_only=True)
	is_liked = serializers.SerializerMethodField(read_only=True)
	class Meta:
		model = Tweet
		fields = ['content', 'timestamp', 'id', 'user', 'likes', 'retweet_obj', 'retweet_count', 'is_liked', 'image']
	
	def get_likes(self, obj):
		return obj.likes.count()

	def get_retweet_obj(self, obj):
		user_name = self.context.get('user_name') if 'user_name' in self.context else self.context.get('request').user
		if obj.retweet_obj != None:
			return TweetDetailSerializer(obj.retweet_obj, context={"user_name": user_name}).data
		else:
			return None

	def get_is_liked(self, obj):
		user_name = self.context.get('user_name') if 'user_name' in self.context else self.context.get('request').user
		user_obj = obj.likes.filter(user_name = user_name)
		return user_obj.exists()

	def get_user(self, obj):
		return UserSerializer(obj.user).data

class TweetCreateSerializer(serializers.ModelSerializer):
	likes = serializers.SerializerMethodField(read_only=True)
	class Meta:
		model = Tweet
		fields = ['content', 'timestamp', 'id', 'likes', 'image', 'image_delete_hash']

	def get_likes(self, obj):
		return obj.likes.count()

	def validate_content(self, value):
		if (len(value) > MAX_TWEET_LENGTH):
			raise serializers.ValidationError("Tweet is longer than max length")
		return value
