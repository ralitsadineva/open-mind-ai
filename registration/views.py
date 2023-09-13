from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.cache import cache
from django.utils import timezone
from datetime import datetime
from .models import JwtToken
import jwt
import redis
import logging

redis_client = cache.client.get_client()

def user_registration_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # email = request.POST['email']
        
        if username and password: # and email:
            try:
                user = User.objects.create_user(username=username, password=password) # , email=email)
            except:
                error_message = "User already exists."
                return render(request, 'registration.html', {'error_message': error_message})
            refresh = RefreshToken.for_user(user)
            new_token = JwtToken.objects.create(user=user, token=str(refresh.access_token))
            cache_key = f'user_tokens:{user.id}'
            redis_client.zadd(cache_key, {new_token.token: new_token.id})
            redis_client.expire(f'{cache_key}:{new_token.token}', 60 * 60 * 24 * 60)
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
            login(request, user)
            # refresh = RefreshToken.for_user(user)
            # JwtToken.objects.create(user=user, token=str(refresh.access_token))
            return redirect('user-tokens')
        else:
            error_message = "Invalid credentials."
            return render(request, 'login.html', {'error_message': error_message})
    
    return render(request, 'login.html')

def user_logout_view(request):
    logout(request)
    return redirect('user-login')

@login_required
def user_tokens_view(request):
    user = request.user
    # tokens = redis_client.smembers(f'user_tokens:{user.id}')
    tokens = redis_client.zrange(f'user_tokens:{user.id}', 0, -1, withscores=True)
    logging.warning(f"Tokens cache: {tokens}")
    if not tokens:
        tokens_obj = JwtToken.objects.filter(user=user)
        tokens = []
        for token in tokens_obj:
            tokens.append((token.token.encode('utf-8'), token.id))
    logging.warning(f"Tokens: {tokens}")
    token_info = []

    for token in tokens:
        access_token = token[0].decode('utf-8')
        token_id = int(token[1])
        try:
            payload = jwt.decode(access_token, options={"verify_signature": False})

            token_expired = payload.get('exp', 0) < timezone.now().timestamp()
            expiration_time = datetime.fromtimestamp(payload.get('exp', 0)).strftime('%Y-%m-%d %H:%M:%S')
        except (jwt.ExpiredSignatureError, jwt.DecodeError):
            token_expired = True
            expiration_time = "Unknown"
        
        token_info.append({
            'token': access_token,
            'expired': token_expired,
            'expiration_time': expiration_time,
            'id': token_id
        })
    
    return render(request, 'user_tokens.html', {'tokens': token_info, 'user': user})

@login_required
def generate_token_view(request):
    user = request.user
    refresh = RefreshToken.for_user(user)
    new_token = JwtToken.objects.create(user=user, token=str(refresh.access_token))
    cache_key = f'user_tokens:{user.id}'
    redis_client.zadd(cache_key, {new_token.token: new_token.id})
    redis_client.expire(f'{cache_key}:{new_token.token}', 60 * 60 * 24 * 60)
    return redirect('user-tokens')

@login_required
def delete_token_view(request, token_id):
    token = get_object_or_404(JwtToken, id=token_id, user=request.user)
    token.delete()
    redis_client.zrem(f'user_tokens:{request.user.id}', token.token)
    return redirect('user-tokens')
