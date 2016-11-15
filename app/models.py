from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
# Create your models here.


class Sport(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField('auth.User')
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    age = models.IntegerField()
    profile_picture = models.FileField()
    fav_sports = models.ManyToManyField(Sport)
    email = models.EmailField(max_length=200)

    def __str__(self):
        return self.first_name + " " + self.last_name

    @property
    def full_name(self):
        return self.first_name + " " + self.last_name


@receiver(post_save, sender="auth.User")
def create_user_profile(**kwargs):
    created = kwargs.get('created')
    instance = kwargs.get('instance')
    if created:
        Profile.objects.create(user=instance)


class Location(models.Model):
    name = models.CharField(max_length=100)
    lat = models.FloatField()
    lng = models.FloatField()

    def __str__(self):
        return self.name


class Event(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(null=True)
    sport = models.ForeignKey(Sport)
    date = models.DateField()
    time = models.TimeField()
    location = models.ForeignKey(Location)
    participants = models.ManyToManyField('auth.User')

    def __str__(self):
        return self.name


class Team(models.Model):
    name = models.CharField(max_length=50)
    home_field = models.ForeignKey(Location)
    players = models.ManyToManyField(Profile)
    logo = models.FileField(null=True)

    def __str__(self):
        return self.name