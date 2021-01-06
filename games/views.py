from django.shortcuts import render
from django.views import *
from django.db.models import Q
from django.shortcuts import render,redirect
from django.contrib import messages
from .models import *
from registration.models import User
from django.views.generic import View
from datetime import date
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from games.models import *
from games.forms import *
from datetime import datetime, timedelta




class GamesList(View):
    def get(self,request):
        games=Game.objects.filter(date=date.today())
        paginator = Paginator(games, 10)
        page = request.GET.get('page')
        try:
            users = paginator.page(page)
        except PageNotAnInteger:
            users = paginator.page(1)
        except EmptyPage:
            users = paginator.page(paginator.num_pages)
        return render(request, 'games/list.html', {'games': games})
class BetsList(View):
    def get(self,request):
        bets=UserBet.objects.filter(user=request.user)
        paginator = Paginator(bets, 10)
        page = request.GET.get('page')
        try:
            bets = paginator.page(page)
        except PageNotAnInteger:
            bets = paginator.page(1)
        except EmptyPage:
            bets = paginator.page(paginator.num_pages)
        return render(request, 'games/bets_list.html', {'bets': bets})
class Revenue(View):
    def get(self,request):
        bets=UserBet.objects.filter(user=request.user).filter(~Q(winner=-1))
        total_revenue = 0
        for game in bets:
            #print(game.winner, request.user,total_revenue)
            if game.winner == request.user:
                total_revenue += game.amount
            else:
                total_revenue-=game.amount
        paginator = Paginator(bets, 10)
        page = request.GET.get('page')

        try:
            bets = paginator.page(page)
        except PageNotAnInteger:
            bets = paginator.page(1)
        except EmptyPage:
            bets = paginator.page(paginator.num_pages)
        return render(request, 'games/revenue.html', {'bets': bets, 'total_revenue':total_revenue})
class BetOnGame(View):
    def get(self,request,game_id):
        if request.user.friends_list().count()==0:
            messages.success(request,"Add friends first")
            return render(request, 'friends_suggestions.html')
        try:
            game=Game.objects.get(id=game_id)
        except Game.DoesNotExist:
            messages.success(request,"Game doesnt exist")
            return redirect('games')
        form = BetonGameForm(game=game,request=request)
        return render(request, 'games/bet_on_game.html', {'game': game,'form': form})

    def post(self,request,game_id):
        game=Game.objects.get(id=game_id)
        form = BetonGameForm(data=request.POST,game=game,request=request)
        if form.is_valid():
            form.cleaned_data['game']=game
            if not form.bet_already_exist(form.cleaned_data):
                bet = form.save(commit=False)
                bet.user=request.user
                bet.game=game
                bet.save()
                messages.success(request, "Bet made successfully")
            else:
                messages.success(request, "Invalid bet")

        return render(request, 'games/bet_on_game.html', {'game': game,'form': form})





