from django.views.generic import View
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import *
from .models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import json


class Login(View):
    def get(self, request):
        form = LoginForm
        return render(request, 'registration/login.html', {'form': form, 'next': request.GET.get('next')})

    def post(self, request):
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = authenticate(email=request.POST['email'], password=request.POST['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)

                    # check if user has no friend then redirect him to suggested friends list
                    if user.friends_list().count() == 0:
                        messages.success(request, "Please add friends before you make a bet")
                        return redirect('friends_suggestions')

                    # otherwise redirect to desired page
                    return redirect(request.POST.get('next'))
                else:
                    #Email().send_activation_email(user, request)
                    messages.info(request, "Account inactive")
            else:
                messages.error(request, "Invalid Login")
        return render(request, 'registration/login.html', {'form': form})


class Logout(View):
    def get(self, request):
        logout(request)
        messages.success(request, "Logged out")
        return redirect('login')


class Register(View):
    def get(self, request):
        form = RegisterForm
        return render(request, 'registration/register.html', {'form': form})

    def post(self, request):
        form = RegisterForm(data=request.POST)
        if form.is_valid():
                user = form.save(commit=False)
                user.set_password(user.password)
                user.save()

                # send activation email
                #Email().send_activation_email(user, request)
                messages.success(request, "Account Registered")
        else:
            return render(request, 'registration/register.html', {'form': form})
        return redirect('login')


class Profile(View):
    def get(self, request):
        form = ProfileForm(instance=request.user)
        return render(request, 'registration/profile.html', {'form': form})

    def post(self, request):
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated")
        return render(request, 'registration/profile.html', {'form': form})





class FriendsSuggestions(View):
    def get(self, request):
        # uncomment this if you want to hide already added friends
        # users = User.objects.filter().exclude(id__in=Friend.objects.filter().values_list('friend_id', flat=True))
        userlist = User.objects.all().exclude(id=request.user.id)
        paginator = Paginator(userlist, 10)
        page = request.GET.get('page')
        try:
            users = paginator.page(page)
        except PageNotAnInteger:
            users = paginator.page(1)
        except EmptyPage:
            users = paginator.page(paginator.num_pages)
        return render(request, 'registration/friends_suggestions.html', {'users': userlist})


# ajax view
class AddFriend(View):
    def get(self, request, friend_id):
        if request.is_ajax():
            try:
                friend = User.objects.get(id=friend_id)
                added = Friend.objects.create(user=request.user, friend=friend)
                if added:
                    return HttpResponse(json.dumps({'status': 'success'}))
                return HttpResponse(json.dumps({'status': 'fail', 'message': "An error occured"}))
            except User.DoesNotExist:
                return HttpResponse(json.dumps({'status': 'fail', 'message': "Invalid Friend"}))
        return HttpResponse('Invalid request')


# ajax view
class RemoveFriend(View):
    def get(self, request, friend_id):
        if request.is_ajax():
            try:
                friend = User.objects.get(id=friend_id)
                friend = Friend.objects.filter(user=request.user, friend=friend)
                if friend.delete():
                    return HttpResponse(json.dumps({'status': 'success'}))
                return HttpResponse(json.dumps({'status': 'fail', 'message': "Something went wrong. Try again."}))
            except User.DoesNotExist:
                return HttpResponse(json.dumps({'status': 'fail', 'message': "Invalid friend"}))
        return HttpResponse('Invalid request')









