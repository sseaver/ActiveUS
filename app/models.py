from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db.models import Avg
from django.conf import settings
from django.contrib.staticfiles.templatetags.staticfiles import static
from rest_framework.authtoken.models import Token
import googlemaps
import os
from datetime import date
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


class Team(models.Model):
    name = models.CharField(max_length=50)
    created_by = models.ForeignKey('auth.User', related_name='captain')
    home_field = models.ForeignKey(Location)
    players = models.ManyToManyField('auth.User')
    logo = models.FileField(blank=True, null=True)

    def __str__(self):
        return self.name

    @property
    def image_url(self):
        if self.logo:
            return self.logo.url
        return static('default.jpg')


VISIBILITY = {
    ('Public', 'Public'),
    ('Private', 'Private')
}


class Event(models.Model):
    name = models.CharField(max_length=50)
    created_by = models.ForeignKey('auth.User', related_name='creator')
    description = models.TextField(null=True)
    sport = models.ForeignKey(Sport)
    date = models.DateField()
    time = models.TimeField()
    location = models.ForeignKey(Location)
    participants = models.ManyToManyField('auth.User', blank=True)
    team = models.ManyToManyField(Team, blank=True)
    visibility = models.CharField(max_length=7, choices=VISIBILITY)

    class Meta:
        ordering = ("date",)

    def __str__(self):
        return self.name

    @property
    def is_public(self):
        return self.visibility == 'Public'

    @property
    def address(self):
        gmaps = googlemaps.Client(key=(os.environ.get('gmapAPIkey')))
        reverse_geocode_result = gmaps.reverse_geocode((self.location.lat, self.location.lng))
        return reverse_geocode_result[0]['formatted_address']

    @property
    def in_future(self):
        if self.date >= date.today():
            return True


class Profile(models.Model):
    user = models.OneToOneField('auth.User')
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    age = models.IntegerField(null=True)
    profile_picture = models.FileField(blank=True, null=True)
    fav_sports = models.ManyToManyField(Sport, blank=True)
    email = models.EmailField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.first_name

    @property
    def full_name(self):
        return self.first_name + " " + self.last_name

    @property
    def image_url(self):
        if self.profile_picture:
            return self.profile_picture.url
        return static('default.jpg')

    def average_rating(self):
        star_dict = Star_Rating.objects.filter(being_rated=self).aggregate(Avg('rating'))
        return round(star_dict['rating__avg'])


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


class Comment(models.Model):
    content = models.TextField()
    relation_user = models.ForeignKey('auth.User')
    relation_event = models.ForeignKey(Event)
    creation_time = models.DateTimeField(auto_now_add=True)
    edit_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content

    class Meta:
        ordering = ("-creation_time",)


class Reply(models.Model):
    content = models.TextField()
    relation_comment = models.ForeignKey(Comment)
    relation_user = models.ForeignKey('auth.User')
    creation_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content
