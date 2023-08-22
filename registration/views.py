from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken
from .models import JwtToken

def user_registration_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # email = request.POST['email']
        
        if username and password: # and email:
            user = User.objects.create_user(username=username, password=password) # , email=email)
            refresh = RefreshToken.for_user(user)
            JwtToken.objects.create(user=user, token=str(refresh.access_token))
            return redirect('user-login')
        else:
            error_message = "Missing required information."
            return render(request, 'registration.html', {'error_message': error_message})
    
    return render(request, 'registration.html')

def user_login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(username=username, password=password)
        if user is not None:
            # login(request, user)
            refresh = RefreshToken.for_user(user)
            JwtToken.objects.create(user=user, token=str(refresh.access_token))
            return redirect('user-tokens')
        else:
            error_message = "Invalid credentials."
            return render(request, 'login.html', {'error_message': error_message})
    
    return render(request, 'login.html')

def user_tokens_view(request):
    user = request.user
    tokens = JwtToken.objects.filter(user=user)
    return render(request, 'user_tokens.html', {'tokens': [token.token for token in tokens]})

def generate_token_view(request):
    user = request.user
    refresh = RefreshToken.for_user(user)
    JwtToken.objects.create(user=user, token=str(refresh.access_token))
    return redirect('user-tokens')
