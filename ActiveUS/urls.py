"""ActiveUS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from rest_framework.authtoken.views import obtain_auth_token
from django.conf.urls.static import static
from app.views import (IndexView, SportCreateView, UserCreateView, ProfileUpdateView, ProfileView,
                       EventCreateView, LocationListCreateAPIView, MapTestView, EventDetailView,
                       EventListView, EventUpdateView, RatingCreateAPIView, OthersProfileView,
                       EventDeleteView, RatingRetrieveAPIView, CommentCreateView,
                       LocationCreateView, CommentUpdateView, TeamCreateView, TeamUpdateView,
                       TeamDetailView, ContactView, EmailUserView)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url('^', include('django.contrib.auth.urls')),
    url(r'^$', IndexView.as_view(), name='index_view'),
    url(r'^create_user/$', UserCreateView.as_view(), name="user_create_view"),
    url(r'^accounts/profile/$', ProfileView.as_view(), name='profile_view'),
    url(r'^accounts/profile/update/$', ProfileUpdateView.as_view(), name='profile_update_view'),
    url(r'^profile/(?P<pk>\d+)/$', OthersProfileView.as_view(), name='others_profile_view'),
    url(r'^sport/create/$', SportCreateView.as_view(), name='sport_create_view'),
    url(r'^event/create/$', EventCreateView.as_view(), name='event_create_view'),
    url(r'^event/(?P<pk>\d+)/$', EventDetailView.as_view(), name='event_detail_view'),
    url(r'^event/(?P<pk>\d+)/update/$', EventUpdateView.as_view(), name='event_update_view'),
    url(r'^event/(?P<pk>\d+)/delete/$', EventDeleteView.as_view(), name='event_delete_view'),
    url(r'^events/$', EventListView.as_view(), name='event_list_view'),
    url(r'^event/(?P<pk>\d+)/comment/create/$', CommentCreateView.as_view(), name='comment_create_view'),
    url(r'^event/(?P<pk>\d+)/comment/(?P<comment_id>\d+)/update/$', CommentUpdateView.as_view(),
        name='comment_update_view'),
    url(r'^team/create/$', TeamCreateView.as_view(), name='team_create_view'),
    url(r'^team/(?P<pk>\d+)/update/$', TeamUpdateView.as_view(), name='team_update_view'),
    url(r'^team/(?P<pk>\d+)/$', TeamDetailView.as_view(), name='team_detail_view'),
    url(r'^location/create', LocationCreateView.as_view(), name='location_create_view'),
    url(r'^api/locations/$', LocationListCreateAPIView.as_view(), name='location_list_create_api_view'),
    url(r'^api/profiles/(?P<pk>\d+)/rating/create/$', RatingCreateAPIView.as_view(), name='rating_create_api_view'),
    url(r'^api/profiles/(?P<pk>\d+)/rating/$', RatingRetrieveAPIView.as_view(), name='rating_retrieve_api_view'),
    url(r'^api/obtain-token/$', obtain_auth_token),
    url(r'^maptest/$', MapTestView.as_view(), name='map_test_view'),
    url(r'^contact/$', ContactView.as_view(), name='contact_view'),
    url(r'^email_user/$', EmailUserView.as_view(), name='email_user_view')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
