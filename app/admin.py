from django.contrib import admin
from app.models import Event, Location, Profile, Sport, Team
# Register your models here.
admin.site.register([Event, Location, Profile, Sport, Team])
