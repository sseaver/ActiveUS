from django.shortcuts import render
from app.models import Profile, Sport
from django.views.generic import TemplateView, DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

# Create your views here.


class IndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self):
        context = super().get_context_data()
        context['login_form'] = AuthenticationForm
        return context


class UserCreateView(CreateView):
    model = User
    form_class = UserCreationForm
    success_url = 'profile_update_view'


class ProfileView(DetailView):
    # model = Profile
    template_name = 'profile_view.html'

    def get_object(self, queryset=None):
        return Profile.objects.get(user=self.request.user)


class ProfileUpdateView(UpdateView):
    model = Profile
    fields = ('first_name', 'last_name', 'age', 'profile_picture', 'fav_sports')


class SportCreateView(CreateView):
    model = Sport
    fields = ("name",)
    success_url = reverse_lazy('index_view')
