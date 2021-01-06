from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone
from datetime import date
from dateutil.relativedelta import relativedelta
from dateutil.parser import parse


class MyUserManager(BaseUserManager):

    def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
        now = timezone.now()
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user = self.model(
            email=email, is_staff=is_staff, is_active=True, is_superuser=is_superuser,
            last_login=now, **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, False, False, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, True, **extra_fields)


class User(AbstractBaseUser):

    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female')
    )

    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    dob = models.DateField(null=True)
    cell = models.CharField(max_length=30, null=True)
    image = models.FileField(null=True, upload_to='')

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now_add=True, null=True)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'

    class Meta:
        db_table = "users"

    def __str__(self):
        return self.name

    def friends_list(self):
        return Friend.objects.filter(user=self)

    def friends_list_ids(self):
        return Friend.objects.filter(user=self).values_list('friend_id', flat=True)


class Friend(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='user')

    # friend will be basically a User from User table
    friend = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='friends')

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        db_table = 'friends'
        ordering = ('-created_at',)

    def __str__(self):
        return self.friend.name



