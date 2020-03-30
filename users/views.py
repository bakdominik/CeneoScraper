from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth


def signup(request):
    if request.method == 'POST':
        # check if passwords are the same
        if request.POST['InputPassword1'] == request.POST['InputPassword2']:
            try:
                # check if username is already in use
                user = User.objects.get(username=request.POST['username'])
                return render(request, 'users/signup.html',{'error':'Ta nazwa użytkownika jest już zajęta'})
            except User.DoesNotExist:
                # create new account if username is not taken
                user = User.objects.create_user(request.POST['username'], password=request.POST['InputPassword1'])
                # login new user
                auth.login(request,user)
                return redirect('home')
        else:
            # raise error passwords doesn't match
            return render(request, 'users/signup.html',{'error':'Hasła nie są identyczne'})
    else:
        return render(request, 'users/signup.html')

def login(request):
    if request.method == 'POST':
        # check if user exists
        user = auth.authenticate(username=request.POST['username'],password=request.POST['InputPassword1'])
        if user is not None:
            # if credentials match login
            auth.login(request, user)
            return redirect('home')
        else:
            return render(request, 'users/login.html',{'error':'Nazwa użytkownika lub hasło są niepoprawne'})
    else:
        return render(request, 'users/login.html')

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect('home')
