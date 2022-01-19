from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

# Create your models here.
class CustomAccountManager(BaseUserManager):

    def create_superuser(self, user_name, first_name, last_name, password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self.create_user(user_name, first_name, last_name, password, **other_fields)

    def create_user(self, user_name, first_name, last_name, password, **other_fields):

        if not user_name:
            raise ValueError(_('You must provide user_name'))

        user = self.model(user_name=user_name, first_name=first_name, last_name=last_name, **other_fields)
        user.set_password(password)
        user.save()
        return user

class User(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(_('email address'), blank=True, null=True)
    user_name = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    start_date = models.DateTimeField(default=timezone.now)
    bio = models.TextField(_('bio'), max_length=500, blank=True)
    is_staff = models.BooleanField(default=False)
    followings = models.ManyToManyField("self", blank=True, symmetrical=False, related_name="followers")
    profile_pic = models.URLField(blank=True, null=True)
    profile_pic_hash = models.CharField(max_length=50, blank=True, null=True)
    objects = CustomAccountManager()

    USERNAME_FIELD = 'user_name'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.user_name