from django import forms
from .models import *

class BetonGameForm(forms.ModelForm):
    amount = forms.DecimalField(max_digits=10, decimal_places=2, min_value=1, help_text='Specify in Dollar')
    friend = forms.ModelChoiceField(queryset=Friend.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}),
                                    help_text='Select your opponent Friend', empty_label='Select friend')
    PART_CHOICES = (
    ('hometeam', 'home_team'),
    ('awayteam', 'away_team'))
    team = forms.ChoiceField(choices=PART_CHOICES,widget=forms.Select(attrs={'class': 'form-control'}),
                                    required=True,label='Select team')
    TYPE_CHOICES=(
    ('point spread','Point Spread'),
    ('straight up','Straight Up')
    )
    type= forms.ChoiceField(choices=PART_CHOICES,widget=forms.Select(attrs={'class': 'form-control'}),
                                    required=True,label='Select bet type')

    class Meta:
        model = UserBet
        fields = ('amount', 'type', 'friend', 'team')

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.game = kwargs.pop('game', None)
        super(BetonGameForm, self).__init__(*args, **kwargs)
        self.fields['friend'].queryset = self.request.user.friends_list()
        x=self.game.Home_team
        y=self.game.Away_team
        PART_CHOICES = (
        (x,x),
        (y,y))
        TYPE_CHOICES=(
        ('point spread','Point Spread'),
        ('straight up','Straight Up')
        )
        #teamchoice=(
        #(self.game.Home_team,self.game.Home_team),
        #(self.game.Away_team,self.game.Away_team))
        self.fields['team'].choices=PART_CHOICES
        self.fields['type'].choices=TYPE_CHOICES

    # here we check if user has already on bet on this team with same friend and game, so we don't allow it again
    def bet_already_exist(self, bet):
        try:
            UserBet.objects.get(friend=bet.get('friend'), team=bet.get('team'), game=bet.get('game'))
            return True
        except UserBet.DoesNotExist:
            return False