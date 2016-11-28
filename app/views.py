from django.shortcuts import render
from app.models import Profile, Sport, Event, Location, Star_Rating, Comment, Team
from django.views.generic import FormView, DetailView, TemplateView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from rest_framework.generics import ListCreateAPIView, CreateAPIView, RetrieveAPIView
from app.serializers import LocationSerializer, RatingSerializer, AvgRatingSerializer
from app.forms import ContactUsForm, ContactUserForm, CreateEventForm
import googlemaps
import os

# Create your views here.


class IndexView(TemplateView):
    template_name = "index.html"
    success_url = reverse_lazy('index_view')

    def get_context_data(self):
        context = super().get_context_data()
        context['login_form'] = AuthenticationForm
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
    form_class = CreateEventForm
    success_url = reverse_lazy('index_view')

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.created_by = self.request.user
        instance.participants = instance.team.players
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        print(kwargs)
        kwargs.update(user=self.request.user)
        return kwargs


class EventDetailView(DetailView):
    model = Event
    template_name = 'event_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        target = Event.objects.get(id=self.kwargs['pk'])
        context['participants'] = target.participants.all()
        context['comments'] = Comment.objects.filter(relation_event=target.id)
        return context

    def post(self, request, pk, **kwargs):
        event_participants = self.request.POST.get('participants')
        event = Event.objects.get(id=pk)
        if event_participants == 'remove_participant':
            event.participants.remove(self.request.user)
        else:
            event.participants.add(self.request.user)
        return HttpResponseRedirect(reverse_lazy('event_detail_view', args=[int(self.kwargs['pk'])]))


class EventUpdateView(UpdateView):
    model = Event
    fields = ("name", "description", "sport", "date", "time", "location", "participants", "visibility")

    def get_success_url(self, **kwargs):
        return reverse_lazy('event_detail_view', args=[int(self.kwargs['pk'])])


class EventListView(ListView):
    model = Event
    template_name = 'events.html'

    def get_queryset(self):
        fav_sports = []
        if not self.request.user.is_authenticated:
            return []
        for sports in self.request.user.profile.fav_sports.all():
            fav_sports.append(sports)
        event_list = Event.objects.filter(sport__in=fav_sports)
        filtered_list = []
        for x in event_list:
            if x.is_public and x.in_future:
                filtered_list.append(x)
        return filtered_list


class EventDeleteView(DeleteView):
    model = Event
    success_url = reverse_lazy('index_view')


class CommentCreateView(CreateView):
    model = Comment
    fields = ('content',)

    def get_success_url(self, **kwargs):
        return reverse_lazy('event_detail_view', args=[int(self.kwargs['pk'])])

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.relation_user = self.request.user
        instance.relation_event = Event.objects.get(id=self.kwargs['pk'])
        return super().form_valid(form)


class CommentUpdateView(UpdateView):
    model = Comment
    fields = ('content',)

    def get_success_url(self, **kwargs):
        return reverse_lazy('event_detail_view', args=[int(self.kwargs['pk'])])


class TeamCreateView(CreateView):
    model = Team
    fields = ('name', 'home_field', 'players', 'logo',)
    success_url = reverse_lazy('index_view')


class TeamUpdateView(UpdateView):
    model = Team
    fields = ('name', 'home_field', 'players', 'logo',)
    success_url = reverse_lazy('index_view')


class TeamDetailView(DetailView):
    model = Team
    template_name = 'team_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        target = Team.objects.get(id=self.kwargs['pk'])
        context['players'] = target.players.all()
        return context


class LocationCreateView(CreateView):
    model = Location
    fields = ('name', 'sport')
    success_url = reverse_lazy('index_view')

    def form_valid(self, form):
        gmaps = googlemaps.Client(key=(os.environ.get('gmapAPIkey')))
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

    def perform_create(self, serializer):
        Star_Rating.objects.filter(rater=self.request.user, being_rated=serializer.validated_data["being_rated"]).delete()
        serializer.save(rater=self.request.user)


class RatingRetrieveAPIView(RetrieveAPIView):
    queryset = Star_Rating.objects.all()
    serializer_class = AvgRatingSerializer


class MapTestView(TemplateView):
    template_name = 'maptest.html'


class EmailUserView(FormView):
    form_class = ContactUserForm
    success_url = reverse_lazy('index_view')
    template_name = 'email_user.html'

    def form_valid(self, form):
        form.send_email()
        return super().form_valid(form)


class ContactView(FormView):
    template_name = 'contact.html'
    success_url = reverse_lazy('index_view')
    form_class = ContactUsForm

    def form_valid(self, form):
        form.send_email()
        return super().form_valid(form)
