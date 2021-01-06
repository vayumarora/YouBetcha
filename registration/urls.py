from django.conf.urls import url
from .views import *
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^login/$', Login.as_view(), name='login'),
    url(r'^logout/$', Logout.as_view(), name='logout'),
    url(r'^register/$', Register.as_view(), name='register'),
    url(r'^profile/$', login_required(Profile.as_view()), name='user_profile'),
    url(r'^friends_suggestions/', FriendsSuggestions.as_view(), name='friends_suggestions'),
    url(r'^add_friend/(?P<friend_id>\d+)/$', login_required(AddFriend.as_view()), name='add_friend'),
    url(r'^remove_friend/(?P<friend_id>\d+)/$', login_required(RemoveFriend.as_view()), name='remove_friend'),
]

