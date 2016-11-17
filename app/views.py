from django.shortcuts import render
from app.models import Profile, Sport, Event, Location, Star_Rating
from django.views.generic import ListView, DetailView, TemplateView, FormView
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView
from app.serializers import LocationSerializer, ProfileSerializer

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
    template_name = 'profile_view.html'

    def get_object(self, queryset=None):
        return Profile.objects.get(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['event'] = Event.objects.filter(participants__id=self.request.user.id).get
        return context


class AjaxableResponseMixin(object):

    def form_invalid(self, form):
        response = super(AjaxableResponseMixin, self).form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        # We make sure to call the parent's form_valid() method because
        # it might do some processing (in the case of CreateView, it will
        # call form.save() for example).
        response = super(AjaxableResponseMixin, self).form_valid(form)
        if self.request.is_ajax():
            data = {
                'pk': self.object.pk,
            }
            return JsonResponse(data)
        else:
            return response


class RatingUpdateView(AjaxableResponseMixin, UpdateView):
    model = Star_Rating
    fields = ('rating',)


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


class EventUpdateView(UpdateView):
    model = Event
    fields = ('participants',)
    success_url = reverse_lazy('profile_view')

    def get_object(self, **kwargs):
        return Event.objects.get(id=self.kwargs['pk'])


class LocationListCreateAPIView(ListCreateAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer


class ProfileUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def get_object(self, **kwargs):
        return Profile.objects.filter(id=self.kwargs['pk'])


class MapTestView(TemplateView):
    template_name = 'maptest.html'
