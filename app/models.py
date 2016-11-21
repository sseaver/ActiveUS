from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings
from rest_framework.authtoken.models import Token
import googlemaps
import os
gmaps = googlemaps.Client(key=(os.environ.get('gmapAPIkey')))

# Create your models here.


class Sport(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Location(models.Model):
    name = models.CharField(max_length=100)
    sport = models.ManyToManyField(Sport)
    lat = models.FloatField()
    lng = models.FloatField()

    def __str__(self):
        return self.name


class Event(models.Model):
    name = models.CharField(max_length=50)
    created_by = models.ForeignKey('auth.User', related_name='creator')
    description = models.TextField(null=True)
    sport = models.ForeignKey(Sport)
    date = models.DateField()
    time = models.TimeField()
    location = models.ForeignKey(Location)
    participants = models.ManyToManyField('auth.User')

    def __str__(self):
        return self.name

    @property
    def address(self):
        reverse_geocode_result = gmaps.reverse_geocode((self.location.lat, self.location.lng))
        return reverse_geocode_result[0]['formatted_address']


class Profile(models.Model):
    user = models.OneToOneField('auth.User')
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    age = models.IntegerField(null=True)
    profile_picture = models.FileField(blank=True, null=True)
    fav_sports = models.ManyToManyField(Sport, blank=True)
    email = models.EmailField(max_length=200, blank=True, null=True)
    events = models.ManyToManyField(Event)

    def __str__(self):
        return self.first_name

    @property
    def full_name(self):
        return self.first_name + " " + self.last_name


@receiver(post_save, sender="auth.User")
def create_user_profile(**kwargs):
    created = kwargs.get('created')
    instance = kwargs.get('instance')
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class Star_Rating(models.Model):
    rater = models.ForeignKey('auth.User')
    being_rated = models.ForeignKey(Profile)
    rating = models.IntegerField()

    @property
    def average_rating(self):
        pass


class Team(models.Model):
    name = models.CharField(max_length=50)
    home_field = models.ForeignKey(Location)
    players = models.ManyToManyField('auth.User')
    logo = models.FileField(null=True)

    def __str__(self):
        return self.name
