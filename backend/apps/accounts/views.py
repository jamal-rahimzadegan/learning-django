from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm


def login_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        print(f"Username: {username}, Password: {password}, User: {user}")

        if user is not None:
            login(request, user)
            return redirect("index")
        else:
            messages.error(request, "Invalid username or password.")
            return redirect("login")

    else:
        return render(request, "accounts/login.html")


def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("index")


def register_user(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
           form.save()
           username = form.cleaned_data.get("username")
           password = form.cleaned_data.get("password1")
           user = authenticate(request, username=username, password=password)
           login(request, user)
           messages.success(request, "Registration successful.")
           return redirect("index")
    else:
          form = UserCreationForm()     
    return render(request, "accounts/register.html", {"form": form})
