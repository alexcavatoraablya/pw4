from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

from .forms import CustomUserLoginForm


# Create your views here.
def user_login(request):
    if request.method == "POST":
        form = CustomUserLoginForm(request.POST)
        if form.is_valid():
            user = authenticate(request,
                                username=form.cleaned_data["username"],
                                password=form.cleaned_data["password"])
            if user is not None:
                login(request, user)
                return redirect("homepage")
    else:
        form = CustomUserLoginForm()
    return render(request, "login.html", {'form': form})

def user_register(request):
    return render(request, "register.html")