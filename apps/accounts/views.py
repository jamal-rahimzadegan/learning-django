from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login


def login_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        print(f"Username: {username}, Password: {password}, User: {user}")

        if user is not None:
            login(request, user)
            return redirect(
                "index"
            )  # Redirect to the index page after successful login
        else:
            messages.error(request, "Invalid username or password.")
            return redirect("login")

    else:
        return render(request, "accounts/login.html")
