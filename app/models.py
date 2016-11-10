from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
# Create your models here.


class Sport(models.Model):
    name = models.CharField(max_length=20)


class Profile(models.Model):
    user = models.ForeignKey('auth.User')
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    age = models.IntegerField()
    fav_sports = models.ManyToManyField(Sport)


@receiver(post_save, sender="auth.User")
def create_user_profile(**kwargs):
    created = kwargs.get('created')
    instance = kwargs.get('instance')
    if created:
        Profile.objects.create(user=instance)


class Location(models.Model):
    name = models.CharField(max_length=100)
    map_url = models.URLField()


class Event(models.Model):
    date = models.DateField(auto_now=False)
    time = models.TimeField(auto_now=False)
    location = models.CharField(max_length=100)
    participants = models.ManyToManyField('auth.User')
