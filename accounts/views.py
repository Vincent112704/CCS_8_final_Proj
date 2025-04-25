from django.shortcuts import render
from .models import userAccount
from django.http import HttpResponse

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password1')
        email = request.POST.get('email')
        password_confirm = request.POST.get('password2')
        if password != password_confirm:
            return render(request, 'accounts/signup.html', {'error': 'Passwords do not match.'})
        if username not in userAccount.objects.values_list('username', flat=True):
            if password not in userAccount.objects.values_list('password', flat=True):
                if email not in userAccount.objects.values_list('email', flat=True):
                    new_user = userAccount(username=username, password=password, email=email)
                    new_user.save()
                    return render(request, 'accounts/signup.html', {'success': True})
                else:
                    return render(request, 'accounts/signup.html', {'error': 'Email already exists.'})
            else:
                return render(request, 'accounts/signup.html', {'error': 'Password already exists.'})
        else: 
            return render(request, 'accounts/signup.html', {'error': 'Username already exists.'})
    return render(request, 'accounts/signup.html')

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = userAccount.objects.filter(username=username, password=password).first()
        if user:
            return render(request, 'accounts/login.html', {'success': True})
        else:
            return render(request, 'accounts/login.html', {'error': 'Invalid username or password.'})
    return render(request, 'accounts/login.html')