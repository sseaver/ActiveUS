from django.shortcuts import render
from app.models import Profile, Sport, Event, Location
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from rest_framework.generics import ListCreateAPIView
from app.serializers import LocationSerializer

# Create your views here.


class IndexView(ListView):
    template_name = "index.html"
    model = Event

    def get_context_data(self):
        context = super().get_context_data()
        context['login_form'] = AuthenticationForm
        return context


class UserCreateView(CreateView):
    model = User
    form_class = UserCreationForm
    success_url = 'profile_update_view'


class ProfileView(DetailView):
    template_name = 'profile_view.html'

    def get_object(self, queryset=None):
        return Profile.objects.get(user=self.request.user)


class ProfileUpdateView(UpdateView):
    model = Profile
    fields = ('first_name', 'last_name', 'age', 'profile_picture', 'fav_sports', 'email')
    success_url = reverse_lazy('profile_view')

    def get_object(self, queryset=None):
        return Profile.objects.get(user=self.request.user)


class SportCreateView(CreateView):
    model = Sport
    fields = ("name",)
    success_url = reverse_lazy('index_view')


class EventCreateView(CreateView):
    model = Event
    fields = ("name", "description", "sport", "date", "time", "location", "participants")
    success_url = reverse_lazy('index_view')


class LocationListCreateAPIView(ListCreateAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer


class MapTestView(TemplateView):
    template_name = 'maptest.html'
