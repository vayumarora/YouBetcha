from django.conf.urls import url
from .views import *
from django.contrib.auth.decorators import login_required



urlpatterns = [
     url(r'^$', login_required(GamesList.as_view()), name='games'),
     url(r'^mybets/$',login_required(BetsList.as_view()), name='bets_list'),
    url(r'^revenue/$',login_required(Revenue.as_view()), name='revenue'),
    url(r'^bet_on_game/(?P<game_id>\d+)/$', login_required(BetOnGame.as_view()), name='bet_on_game'),
    ]