from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("/dashboard")
        else:
            return render(request, 'login.html', {'form': AuthenticationForm()})

    if request.user.is_authenticated:
        return render(request, 'index.html')

    return render(request, 'login.html', {'form': AuthenticationForm()})


def logout_view(request):
    logout(request)
    return render(request, 'login.html', {'form': AuthenticationForm()})
