from django.shortcuts import render
from app.models import Profile, Sport, Event, Location, Star_Rating
from django.views.generic import FormView, DetailView, TemplateView, View, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from rest_framework.generics import ListCreateAPIView, CreateAPIView, RetrieveAPIView
from app.serializers import LocationSerializer, RatingSerializer
import googlemaps
import os
gmaps = googlemaps.Client(key=(os.environ.get('gmapAPIkey')))

# Create your views here.


class IndexView(TemplateView):
    template_name = "index.html"
    success_url = reverse_lazy('index_view')

    def get_context_data(self):
        context = super().get_context_data()
        context['login_form'] = AuthenticationForm
        context['event'] = Event.objects.all()
        return context


class UserCreateView(FormView):
    template_name = 'auth/user_form.html'
    model = User
    form_class = UserCreationForm
    success_url = reverse_lazy('profile_update_view')

    def form_valid(self, form):
        form.save()
        username = self.request.POST['username']
        password = self.request.POST['password1']
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return super(UserCreateView, self).form_valid(form)


class ProfileView(DetailView):
    model = Event
    template_name = 'profile_view.html'

    def get_object(self, queryset=None):
        return Profile.objects.get(user=self.request.user)


class OthersProfileView(DetailView):
    template_name = "profile_view.html"

    def get_object(self, **kwargs):
        return Profile.objects.get(id=self.kwargs['pk'])


class RatingUpdateView(View):
    pass


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


class EventDetailView(DetailView):
    model = Event
    template_name = 'event_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        target = Event.objects.get(id=self.kwargs['pk'])
        context['participants'] = target.participants.all()
        return context


class EventUpdateView(UpdateView):
    model = Event
    success_url = reverse_lazy('event_detail_view')


class EventDeleteView(DeleteView):
    model = Event
    success_url = reverse_lazy('index_view')


class EventParticipantsUpdateView(UpdateView):
    model = Event
    fields = ('participants',)
    success_url = reverse_lazy('profile_view')

    def get_object(self, **kwargs):
        return Event.objects.get(id=self.kwargs['pk'])

    def post(self, request, pk):
        participants = self.request.POST.get('participants')
        event = Event.objects.get(id=pk)
        if participants == 'remove_participant':
            event.participants.remove(user=self.request.user)
        else:
            event.participants.add(user=self.request.user)
        return HttpResponseRedirect(reverse_lazy('event_detail_view'))


class LocationCreateView(CreateView):
    model = Location
    fields = ('name', 'sport')
    success_url = reverse_lazy('index_view')

    def form_valid(self, form):
        instance = form.save(commit=False)
        address = self.request.POST['address']
        geocode_result = gmaps.geocode(address)
        lat_lng_dict = geocode_result[0]['geometry']['location']
        latitude = lat_lng_dict['lat']
        longitude = lat_lng_dict['lng']
        instance.lat = latitude
        instance.lng = longitude
        return super().form_valid(form)


class LocationListCreateAPIView(ListCreateAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer


class RatingCreateAPIView(CreateAPIView):
    queryset = Star_Rating.objects.all()
    serializer_class = RatingSerializer

    def post(self, request, pk):
        rating = self.request.POST.get('voting')
        profile = Profile.objects.get(id=pk)
        Star_Rating.objects.create(rater=self.request.user, being_rated=profile, rating=rating)
        return HttpResponseRedirect(reverse('profile_view'))


class RatingRetrieveAPIView(RetrieveAPIView):
    queryset = Star_Rating.objects.all()
    serializer_class = RatingSerializer


class MapTestView(TemplateView):
    template_name = 'maptest.html'
