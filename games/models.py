from django.db import models
from games.models import *
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
from registration.models import *

class Team(models.Model):
    name=models.CharField(max_length=200)
    sport=models.CharField(max_length=50,default="NBA")

    class Meta:
        db_table='team'
    def __str__(self):
        return self.name
class Game(models.Model):
    sport = models.CharField(max_length=50)
    date = models.DateField(max_length=50)
    time = models.CharField(max_length=100)
    Home_team = models.CharField(max_length=50)
    Away_team = models.CharField(max_length=50)
    Home_line =models.CharField(max_length=50,null=True)
    Away_line =models.CharField(max_length=50,null=True)
    #Home_line = models.DecimalField(max_digits=5,decimal_places=2,null=True)
    #Away_line = models.DecimalField(max_digits=5,decimal_places=2,null=True)
    Home_preview=models.URLField(max_length=500)
    Away_preview=models.URLField(max_length=500)
    class Meta:
        db_table='game'
        ordering=('date','time')
    def __unicode__(self):
        #return (BettingInfo.Home_team,BettingInfo.date)
        return self.date
class Result(models.Model):
    Home_team= models.CharField(max_length=50, default='A')
    Away_team=models.CharField(max_length=50,default='A')
    Home_points=models.PositiveIntegerField(default=0)
    Away_points=models.PositiveIntegerField(default=0)
    game=models.OneToOneField(Game,on_delete=models.DO_NOTHING,related_name='game')
    class Meta:
        db_table='results'

class UserBet(models.Model):
    TYPE_CHOICES=(
    ('point spread','Point Spread'),
    ('straight up','Straight Up')
    )
    amount=models.DecimalField(max_digits=10,decimal_places=2)
    type = models.CharField(max_length=50, choices=TYPE_CHOICES, default='point spread')

    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='bet_user')
    friend = models.ForeignKey(Friend,on_delete=models.DO_NOTHING, related_name='bet_friend')

    game = models.ForeignKey(Game, on_delete=models.DO_NOTHING, related_name='bet_game')
    team=models.CharField(max_length=50)
    winner=models.ForeignKey(User, default = -1, on_delete=models.DO_NOTHING, related_name=None)

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now_add=True, null=True)


    class Meta:
        db_table = 'user_bets'
        ordering = ('-created_at',)
