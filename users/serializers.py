from django.db import models
from django.db.models import fields
from rest_framework import serializers
from .models import User

class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_name', 'first_name', 'last_name', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user_instance = self.Meta.model(**validated_data)
        if password is not None:
            user_instance.set_password(password)
        user_instance.save()
        return user_instance

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_name', 'first_name', 'last_name']

class UserDetailsSerializer(serializers.ModelSerializer):
    followers_count = serializers.SerializerMethodField()
    followings_count = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ['user_name', 'first_name', 'last_name', 'id', 'bio', 'is_staff', 'followers_count', 'followings_count']
    
    def get_followers_count(self, obj):
        return obj.followers.count()
    
    def get_followings_count(self, obj):
        return obj.followings.count()